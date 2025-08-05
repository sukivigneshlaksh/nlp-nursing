import langextract as lx
from google import genai
from google.genai.types import HttpOptions, Part
import vertexai
from typing import Dict, List, Any
import json
from dotenv import load_dotenv
import os

load_dotenv()

# Configuration matching existing project patterns
PROJECT_ID = "suki-dev"
LOCATION = "us-central1"

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)
client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION,
    http_options=HttpOptions(api_version="v1")
)

# 1. Form Structure Extraction using Vertex AI (matching form_processor.py pattern)
def extract_form_structure(pdf_path: str) -> Dict[str, Any]:
    """Extract form structure from PDF using Vertex AI GenAI"""
    prompt = """
Extract the form structure from this medical form PDF and return as JSON schema.

Please identify:
- Field names and their types (text, date, medication, condition, etc.)
- Field categories and sections
- Required vs optional fields
- Current values if any are filled

Return JSON in this format:
{
    "form_metadata": {
        "form_id": "...",
        "form_title": "...", 
        "form_type": "..."
    },
    "fields": {
        "field_name": {
            "type": "field_type",
            "required": true/false,
            "current_value": "...",
            "section": "..."
        }
    },
    "field_types": {
        "field_name": "field_type"
    }
}
"""
    
    try:
        with open(pdf_path, "rb") as f:
            pdf_data = f.read()

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                prompt,
                Part.from_bytes(
                    data=pdf_data,
                    mime_type="application/pdf"
                )
            ]
        )
        
        # Clean response similar to medical_form_utils.py
        text = response.text.strip()
        if text.startswith('```'):
            text = text.split('\n', 1)[1].rsplit('\n', 1)[0]
        
        return json.loads(text)
        
    except Exception as e:
        print(f"Error extracting form structure: {e}")
        return {"fields": {}, "field_types": {}}

def infer_field_type(field_name: str) -> str:
    """Infer field type from field name"""
    field_name_lower = field_name.lower()
    
    if any(term in field_name_lower for term in ["date", "dob", "birth"]):
        return "date"
    elif any(term in field_name_lower for term in ["medication", "drug", "med"]):
        return "medication"
    elif any(term in field_name_lower for term in ["dose", "dosage", "amount"]):
        return "dosage"
    elif any(term in field_name_lower for term in ["condition", "diagnosis", "symptom"]):
        return "condition"
    elif any(term in field_name_lower for term in ["name", "patient"]):
        return "text"
    else:
        return "text"

# 2. Semantic Content Parsing using LangExtract (matching existing patterns)
def extract_medical_entities(text: str) -> List[Dict[str, Any]]:
    """Extract medical entities from text transcript using LangExtract with source grounding"""
    
    # Get API key from environment like lang_extract_test.py
    api_key = os.getenv('LANGEXTRACT_API_KEY')
    
    prompt_description = """Extract medical information including patient names, medications, dosages, 
    conditions, dates, vital signs, addresses, phone numbers, and insurance information 
    in the order they appear in the text. Use exact text for extractions."""
    
    # Enhanced examples based on the actual CMS transcript patterns
    examples = [
        lx.data.ExampleData(
            text="Patient John David Smith, DOB May 15th, 1968, address 123 Maple Street, Anytown, California 90210, phone (555) 123-4567. Medicare ID 1A2B-3C4D-5E6F. Height 70 inches, weight 220 pounds. Diagnosed with obstructive sleep apnea. AHI was 28.5. Initial evaluation October 26th, 2023. Sleep study September 20th, 2023.",
            extractions=[
                lx.data.Extraction(extraction_class="patient_name", extraction_text="John David Smith"),
                lx.data.Extraction(extraction_class="date_of_birth", extraction_text="May 15th, 1968"),
                lx.data.Extraction(extraction_class="address", extraction_text="123 Maple Street, Anytown, California 90210"),
                lx.data.Extraction(extraction_class="phone", extraction_text="(555) 123-4567"),
                lx.data.Extraction(extraction_class="insurance_id", extraction_text="1A2B-3C4D-5E6F"),
                lx.data.Extraction(extraction_class="height", extraction_text="70 inches"),
                lx.data.Extraction(extraction_class="weight", extraction_text="220 pounds"),
                lx.data.Extraction(extraction_class="condition", extraction_text="obstructive sleep apnea"),
                lx.data.Extraction(extraction_class="vital_measurement", extraction_text="AHI was 28.5"),
                lx.data.Extraction(extraction_class="evaluation_date", extraction_text="October 26th, 2023"),
                lx.data.Extraction(extraction_class="study_date", extraction_text="September 20th, 2023")
            ]
        )
    ]
    
    result = lx.extract(
        text_or_documents=text,
        prompt_description=prompt_description,
        examples=examples,
        model_id="gemini-2.5-pro",
        api_key=api_key,
        max_workers=8M
    )
    
    entities = []
    for entity in result.extractions:
        entities.append({
            "type": entity.extraction_class,
            "text": entity.extraction_text,
            "source_position": {
                "start": entity.char_interval.start_pos if entity.char_interval else None,
                "end": entity.char_interval.end_pos if entity.char_interval else None
            },
            "attributes": entity.attributes if hasattr(entity, 'attributes') else {}
        })
    
    return entities

# 3. Form Filling Logic
def map_entities_to_form(entities: List[Dict[str, Any]], form_schema: Dict[str, Any]) -> Dict[str, Any]:
    """Map extracted entities to form fields based on field types"""
    
    filled_form = {}
    
    # Group entities by type
    entity_groups = {}
    for entity in entities:
        entity_type = entity["type"]
        if entity_type not in entity_groups:
            entity_groups[entity_type] = []
        entity_groups[entity_type].append(entity)
    
    # Map entities to form fields
    for field_name, field_info in form_schema["fields"].items():
        field_type = field_info["type"]
        
        # Direct type matching
        if field_type in entity_groups and entity_groups[field_type]:
            filled_form[field_name] = entity_groups[field_type][0]["text"]
        
        # Smart mapping based on field names
        elif field_type == "text":
            if "patient" in field_name.lower() and "patient_name" in entity_groups:
                filled_form[field_name] = entity_groups["patient_name"][0]["text"]
        
        # Keep existing value if no match found
        else:
            filled_form[field_name] = field_info.get("current_value", "")
    
    return filled_form

# Integration with existing project utilities
def load_existing_form_template(form_type: str = "CMS") -> Dict[str, Any]:
    """Load existing form template from outputs directory"""
    try:
        file_mapping = {
            "CMS": "../outputs/cms_output.json",
            "OASIS": "../outputs/oasis_output_short.json"
        }
        
        file_path = file_mapping.get(form_type, "../outputs/cms_output.json")
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Template file not found for {form_type}")
        return {}

def load_existing_transcript(form_type: str = "CMS") -> str:
    """Load existing sample transcript"""
    try:
        file_mapping = {
            "CMS": "../outputs/sample_scripts/cms_sample_transcript.txt",
            "OASIS": "../outputs/sample_scripts/oasis_short_sample_transcript.txt"
        }
        
        file_path = file_mapping.get(form_type, "../outputs/sample_scripts/cms_sample_transcript.txt")
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Clean formatting like medical_form_utils.py
        content = content.replace("**", "").replace("*", "")
        lines = [line.strip() for line in content.split('\n') 
                if line.strip() and not line.startswith('---')]
        
        return '\n\n'.join(lines)
        
    except FileNotFoundError:
        return "Sample transcript not found."

# Main execution with real project data
def main():
    print("=== Medical Form Processing Pipeline ===\n")
    
    # Use existing project data
    form_type = "CMS"  # Can be changed to "OASIS"
    template = load_existing_form_template(form_type)
    transcript = load_existing_transcript(form_type)
    
    print(f"Processing {form_type} form with existing data...\n")
    
    # Step 1: Form structure (using existing template as schema)
    print("1. Form Structure (sample fields):")
    sample_fields = {}
    if "section_a" in template and "patient_information" in template["section_a"]:
        sample_fields = template["section_a"]["patient_information"]
    print(json.dumps(sample_fields, indent=2))
    
    # Step 2: Extract entities from transcript  
    print("\n2. Extracting entities from transcript...")
    print(f"Transcript preview: {transcript[:200]}...\n")
    
    entities = extract_medical_entities(transcript)
    print("Extracted entities:")
    for entity in entities:
        pos_info = ""
        if entity["source_position"]["start"] is not None:
            pos_info = f" (pos: {entity['source_position']['start']}-{entity['source_position']['end']})"
        print(f"• {entity['type']}: {entity['text']}{pos_info}")
    
    # Step 3: Create simplified mapping for demonstration
    print("\n3. Entity-to-Field Mapping Example:")
    entity_mapping = {}
    for entity in entities:
        if entity["type"] == "patient_name":
            entity_mapping["patient_name"] = entity["text"]
        elif entity["type"] == "date_of_birth":
            entity_mapping["dob"] = entity["text"]
        elif entity["type"] == "address":
            entity_mapping["address"] = entity["text"]
        elif entity["type"] == "phone":
            entity_mapping["telephone"] = entity["text"]
        elif entity["type"] == "insurance_id":
            entity_mapping["hicn"] = entity["text"]
    
    print("Mapped fields:")
    print(json.dumps(entity_mapping, indent=2))
    
    # Step 4: Save results for integration
    output_file = f"lang_extract_{form_type.lower()}_results.json"
    results = {
        "form_type": form_type,
        "extracted_entities": entities,
        "mapped_fields": entity_mapping,
        "processing_timestamp": "2024-01-01T00:00:00Z" # lol?
    }
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved to: {output_file}")
    
    # Generate visualization like original lang_extract_test.py
    try:
        # Save annotated documents for visualization
        result_obj = type('Result', (), {
            'extractions': [
                type('Extraction', (), {
                    'extraction_class': e['type'],
                    'extraction_text': e['text'],
                    'char_interval': type('Interval', (), {
                        'start_pos': e['source_position']['start'],
                        'end_pos': e['source_position']['end']
                    })() if e['source_position']['start'] is not None else None
                })() for e in entities
            ]
        })()
        
        lx.io.save_annotated_documents([result_obj], output_name="medical_form_extraction.jsonl", output_dir=".")
        
        html_content = lx.visualize("medical_form_extraction.jsonl")
        with open("medical_form_visualization.html", "w") as f:
            f.write(html_content)
        
        print("✓ Interactive visualization saved to medical_form_visualization.html")
        
    except Exception as e:
        print(f"Note: Visualization generation skipped - {e}")

if __name__ == "__main__":
    main()