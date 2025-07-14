"""
Simple PDF Form Processor
Uses only Vertex AI with direct PDF processing.
"""

import json
import base64
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

import vertexai
from vertexai.generative_models import GenerativeModel, Part

# Initialize Vertex AI
vertexai.init(project="suki-dev", location="us-central1")
model = GenerativeModel("gemini-1.5-pro")

def create_pdf_part(pdf_path: str) -> Part:
    """Create a Part object from PDF file for direct model processing"""
    with open(pdf_path, "rb") as f:
        pdf_data = base64.b64encode(f.read()).decode()
    
    return Part.from_data(
        data=pdf_data,
        mime_type="application/pdf"
    )

def create_form_structure(pdf_path: str, form_name: str) -> dict:
    """Step 1: PDF → JSON structure"""
    print(f"Step 1: Creating structure for {form_name}...")
    
    pdf_part = create_pdf_part(pdf_path)
    
    prompt = f"""
    Analyze this PDF form and create a JSON structure with empty fields:
    
    INSTRUCTIONS:
    1. Identify all form fields (text inputs, checkboxes, text areas, etc.)
    2. Create appropriate field types and labels
    3. Set all values to null
    4. Group related fields into logical sections
    
    Return ONLY a JSON structure like:
    {{
      "form_name": "{form_name}",
      "sections": [
        {{
          "section_name": "patient_info",
          "fields": [
            {{
              "field_name": "patient_name",
              "label": "Patient Name",
              "field_type": "text_input",
              "value": null
            }}
          ]
        }}
      ]
    }}
    """
    
    response = model.generate_content([pdf_part, prompt])
    
    try:
        text = response.text.strip()
        if text.startswith("```"):
            lines = text.split('\n')
            text = '\n'.join(lines[1:-1])
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "form_name": form_name,
            "sections": [],
            "error": "Failed to create structure"
        }

def fill_form_structure(structure_json: dict, transcript: str) -> dict:
    """Step 2: JSON + transcript → filled JSON"""
    form_name = structure_json.get("form_name", "unknown")
    print(f"Step 2: Filling structure for {form_name}...")
    
    prompt = f"""
    Fill this form structure using the provided transcript:
    
    FORM STRUCTURE:
    {json.dumps(structure_json, indent=2)}
    
    TRANSCRIPT:
    {transcript}
    
    INSTRUCTIONS:
    1. Fill ONLY the "value" fields using information from the transcript
    2. If information not available in transcript, keep value as null
    3. Match data types appropriately
    4. Preserve the entire structure, only change "value" fields
    
    Return the same JSON structure with filled values.
    """
    
    response = model.generate_content([prompt])
    
    try:
        text = response.text.strip()
        if text.startswith("```"):
            lines = text.split('\n')
            text = '\n'.join(lines[1:-1])
        return json.loads(text)
    except json.JSONDecodeError:
        structure_json["fill_error"] = "Failed to fill form"
        return structure_json

def process_pdf_complete(pdf_path: str, transcript: str, form_name: str = None) -> dict:
    """Complete workflow: PDF → structure → filled form"""
    if not form_name:
        form_name = Path(pdf_path).stem
    
    # Step 1: Create structure
    structure = create_form_structure(pdf_path, form_name)
    
    # Step 2: Fill structure
    filled_form = fill_form_structure(structure, transcript)
    
    return {
        "form_name": form_name,
        "pdf_path": pdf_path,
        "structure": structure,
        "filled_form": filled_form,
        "transcript": transcript
    }

if __name__ == "__main__":
    # Test the processor
    try:
        from form_transcripts import SIMPLE_FORM_TRANSCRIPT
        
        pdf_path = "../data/pdf/Simple_Form.pdf"
        
        print("=== Testing Simple Processor ===")
        print(f"Processing: {pdf_path}")
        print(f"Transcript length: {len(SIMPLE_FORM_TRANSCRIPT)} characters")
        
        # Test the complete workflow
        result = process_pdf_complete(pdf_path, SIMPLE_FORM_TRANSCRIPT)
        
        print(f"\nResults:")
        print(f"Form name: {result['form_name']}")
        print(f"Structure sections: {len(result['structure'].get('sections', []))}")
        print(f"Filled sections: {len(result['filled_form'].get('sections', []))}")
        
        # Show sample of extracted fields
        filled_sections = result['filled_form'].get('sections', [])
        if filled_sections:
            print(f"\nSample extracted fields:")
            for section in filled_sections[:2]:  # Show first 2 sections
                section_name = section.get('section_name', 'unknown')
                fields = section.get('fields', [])
                filled_fields = [f for f in fields if f.get('value') is not None]
                print(f"  {section_name}: {len(filled_fields)} filled fields")
                
                # Show first few filled fields
                for field in filled_fields[:3]:
                    label = field.get('label', 'Unknown')
                    value = str(field.get('value', ''))[:50]
                    print(f"    {label}: {value}")
        
        # Save result for inspection
        outputs_dir = Path("outputs/simple")
        outputs_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = outputs_dir / "test_result.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"\nFull result saved to: {output_file}")
        print("Test completed successfully!")
        
    except ImportError:
        print("Error: Could not import form_transcripts")
        print("Make sure form_transcripts.py exists with SIMPLE_FORM_TRANSCRIPT")
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        print("Make sure the PDF file exists at the specified path")
    except Exception as e:
        print(f"Error during processing: {e}")
        import traceback
        traceback.print_exc()