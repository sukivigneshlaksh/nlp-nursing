import json
import os
from dotenv import load_dotenv
import openai
from form_files_2.vibra_ltac import VibraLTACProgressNote, sample_vibra_ltac_transcript
from form_files_2.vibra_irf import VibraIRFProgressNote, sample_vibra_irf_transcript
from form_files_2.vibra_physical import VibraIRFHistoryPhysical, sample_vibra_irf_hp_transcript
from form_files_2.medical_consult import MedicalConsult, sample_medical_consult_transcript
from form_files_2.ltac_history import VibraLTACHistoryPhysical, sample_vibra_ltac_hp_transcript
from form_files_2.bh_history import GeneralHistoryPhysical, sample_general_hp_transcript

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Form configurations
FORMS = {
    "Vibra LTAC Progress Note": {
        "model": VibraLTACProgressNote,
        "transcript": sample_vibra_ltac_transcript
    },
    "Vibra IRF Progress Note": {
        "model": VibraIRFProgressNote,
        "transcript": sample_vibra_irf_transcript
    },
    "Vibra IRF History & Physical": {
        "model": VibraIRFHistoryPhysical,
        "transcript": sample_vibra_irf_hp_transcript
    },
    "Medical Consult": {
        "model": MedicalConsult,
        "transcript": sample_medical_consult_transcript
    },
    "Vibra LTAC History & Physical": {
        "model": VibraLTACHistoryPhysical,
        "transcript": sample_vibra_ltac_hp_transcript
    },
    "General History & Physical": {
        "model": GeneralHistoryPhysical,
        "transcript": sample_general_hp_transcript
    }
}

def extract_medical_data(transcript, model_class):
    """Extract structured medical data from transcript using OpenAI API"""
    response = client.beta.chat.completions.parse(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Extract medical form data from transcript. Only use explicitly mentioned information."},
            {"role": "user", "content": transcript}
        ],
        response_format=model_class,
    )
    return response.choices[0].message.parsed

def evaluate_extraction_quality(extracted_data, form_type, original_transcript):
    """Evaluate the quality of extracted medical data against original transcript"""
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are a medical documentation quality expert. Compare the extracted data against the original transcript to rate extraction accuracy, completeness, and clinical relevance on a 1-100 scale."},
            {"role": "user", "content": f"Form Type: {form_type}\n\nOriginal Transcript: {original_transcript}\n\nExtracted Data: {json.dumps(extracted_data, indent=2)}\n\nProvide: Score (1-100), Key Strengths (2-3 points), Areas for Improvement (1-2 points)"}
        ],
        max_tokens=300
    )
    return response.choices[0].message.content

def save_results_to_file(form_name, extracted_data, quality_evaluation, filename):
    """Save extracted data and quality evaluation to JSON file"""
    result = {
        "form_type": form_name,
        "extracted_data": extracted_data.model_dump(),
        "quality_evaluation": quality_evaluation
    }
    
    # Create outputs directory if it doesn't exist
    os.makedirs("outputs", exist_ok=True)
    
    # Save to outputs directory
    filepath = os.path.join("outputs", filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Results saved to {filepath}")

def process_form(form_name):
    """Process a single form and save results"""
    form_config = FORMS[form_name]
    
    print(f"Processing {form_name}...")
    
    try:
        # Extract medical data
        extracted_data = extract_medical_data(form_config["transcript"], form_config["model"])
        print(f"✓ Extraction complete")
        
        # Evaluate extraction quality
        quality_evaluation = evaluate_extraction_quality(extracted_data.model_dump(), form_name, form_config["transcript"])
        print(f"✓ Quality evaluation complete")
        
        # Create filename - replace spaces and special characters
        filename = f"{form_name.lower().replace(' ', '_').replace('&', 'and')}_results.json"
        
        # Save to file
        save_results_to_file(form_name, extracted_data, quality_evaluation, filename)
        
        print(f"✓ {form_name} processing complete")
        
        # Print quality evaluation summary
        print(f"📊 Quality Evaluation:")
        print(f"   {quality_evaluation}")
        
    except Exception as e:
        print(f"✗ {form_name} processing failed: {str(e)}")

def process_specific_forms(form_names):
    """Process only specific forms"""
    print("Medical Form Processor - Selected Forms")
    print("=" * 50)
    
    for form_name in form_names:
        if form_name in FORMS:
            process_form(form_name)
            print()
        else:
            print(f"⚠ Form '{form_name}' not found in available forms")
            print(f"Available forms: {list(FORMS.keys())}")

def main():
    """Process all forms or selected forms"""
    print("Medical Form Processor - All Vibra Forms")
    print("=" * 50)
    
    # Process all forms
    for form_name in FORMS.keys():
        process_form(form_name)
        print()
    
    print("=" * 50)
    print(f"Processed {len(FORMS)} forms total")
    print("All results saved to outputs/ directory")

def list_available_forms():
    """List all available forms"""
    print("Available Forms:")
    print("=" * 30)
    for i, form_name in enumerate(FORMS.keys(), 1):
        print(f"{i}. {form_name}")

if __name__ == "__main__":
    # Uncomment the line below to see available forms
    # list_available_forms()
    
    # Process all forms
    main()
    
    # Or process specific forms:
    # process_specific_forms(["Vibra LTAC Progress Note", "Medical Consult"])