"""
Mono Utils - Minimal consolidated utilities for NLP Nursing project
"""

import json
import os
from typing import Dict, List, Any
from dotenv import load_dotenv
from google import genai
from google.genai.types import HttpOptions, Part
import vertexai
import langextract as lx

load_dotenv()

# =============================================================================
# CONFIG
# =============================================================================

PROJECT_ID = "suki-dev"
LOCATION = "us-central1"
GEMINI_MODEL = "gemini-2.5-flash"
LANGEXTRACT_API_KEY = os.getenv('LANGEXTRACT_API_KEY')

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)
client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION,
    http_options=HttpOptions(api_version="v1")
)

# =============================================================================
# FILE I/O
# =============================================================================

def load_json(file_path: str) -> Dict[str, Any]:
    """Load JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except:
        return {}

def load_template(form_type: str = "CMS") -> Dict[str, Any]:
    """Load form template"""
    paths = {
        "CMS": "../outputs/cms_output.json",
        "OASIS": "../outputs/oasis_output_short.json"
    }
    return load_json(paths.get(form_type, paths["CMS"]))

def load_transcript(form_type: str = "CMS") -> str:
    """Load sample transcript"""
    paths = {
        "CMS": "../outputs/sample_scripts/cms_sample_transcript.txt",
        "OASIS": "../outputs/sample_scripts/oasis_short_sample_transcript.txt"
    }
    
    try:
        with open(paths.get(form_type, paths["CMS"]), 'r') as f:
            content = f.read()
        # Clean formatting
        content = content.replace("**", "").replace("*", "")
        lines = [line.strip() for line in content.split('\n') 
                if line.strip() and not line.startswith('---')]
        return '\n\n'.join(lines)
    except:
        return "Transcript not found"

# =============================================================================
# AI UTILITIES
# =============================================================================

def clean_ai_response(text: str) -> str:
    """Remove markdown code blocks"""
    text = text.strip()
    if text.startswith('```'):
        text = text.split('\n', 1)[1].rsplit('\n', 1)[0]
    return text

def generate_with_ai(prompt: str, pdf_data: bytes = None) -> str:
    """Generate content with Vertex AI"""
    contents = [prompt]
    if pdf_data:
        contents.append(Part.from_bytes(data=pdf_data, mime_type="application/pdf"))
    
    response = client.models.generate_content(model=GEMINI_MODEL, contents=contents)
    return clean_ai_response(response.text)

# =============================================================================
# LANGEXTRACT
# =============================================================================

def extract_medical_entities(text: str) -> List[Dict[str, Any]]:
    """Extract medical entities using LangExtract"""
    
    prompt = """Extract medical information including patient names, medications, dosages, 
    conditions, dates, vital signs, addresses, phone numbers, and insurance information."""
    
    examples = [
        lx.data.ExampleData(
            text="Patient John Smith, DOB May 15, 1968, address 123 Main St, phone (555) 123-4567. Diagnosed with sleep apnea.",
            extractions=[
                lx.data.Extraction(extraction_class="patient_name", extraction_text="John Smith"),
                lx.data.Extraction(extraction_class="date_of_birth", extraction_text="May 15, 1968"),
                lx.data.Extraction(extraction_class="address", extraction_text="123 Main St"),
                lx.data.Extraction(extraction_class="phone", extraction_text="(555) 123-4567"),
                lx.data.Extraction(extraction_class="condition", extraction_text="sleep apnea")
            ]
        )
    ]
    
    result = lx.extract(
        text_or_documents=text,
        prompt_description=prompt,
        examples=examples,
        model_id="gemini-2.5-pro",
        api_key=LANGEXTRACT_API_KEY,
        max_workers=8
    )
    
    entities = []
    for entity in result.extractions:
        entities.append({
            "type": entity.extraction_class,
            "text": entity.extraction_text,
            "source_position": {
                "start": entity.char_interval.start_pos if entity.char_interval else None,
                "end": entity.char_interval.end_pos if entity.char_interval else None
            }
        })
    
    return entities

# =============================================================================
# FORM PROCESSING
# =============================================================================

def extract_with_citations(transcript: str, template: Dict, form_type: str) -> Dict:
    """Extract data into form template with citations"""
    prompt = f"""Fill this {form_type} form using ONLY information from the transcript.

TEMPLATE: {json.dumps(template, indent=2)}

TRANSCRIPT: {transcript}

Rules:
- Only use information explicitly mentioned
- If not mentioned → leave empty
- Provide exact quotes as citations

Return JSON:
{{
    "filled_form": {{ /* filled template */ }},
    "citations": {{
        "field.path": {{
            "value": "extracted value",
            "source_quote": "exact quote",
            "confidence": 8
        }}
    }}
}}"""
    
    response = generate_with_ai(prompt)
    try:
        return json.loads(response)
    except:
        return {"filled_form": {}, "citations": {}}

def process_pdf_form(pdf_path: str) -> Dict[str, Any]:
    """Extract structure from PDF form"""
    prompt = """Extract form structure as JSON with field names, types, and current values."""
    
    try:
        with open(pdf_path, "rb") as f:
            pdf_data = f.read()
        response = generate_with_ai(prompt, pdf_data)
        return json.loads(response)
    except:
        return {}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_field_values(obj: Dict, prefix: str = "") -> Dict[str, str]:
    """Extract all field values from nested JSON"""
    fields = {}
    if isinstance(obj, dict):
        for key, value in obj.items():
            path = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                fields.update(get_field_values(value, path))
            elif value and str(value).strip():
                fields[path] = str(value)
    return fields

def format_field_name(field_name: str) -> str:
    """Clean field names for display"""
    return field_name.replace("_", " ").replace(".", " → ").title()

# =============================================================================
# QUICK FUNCTIONS
# =============================================================================

def quick_extract(transcript: str, form_type: str = "CMS") -> Dict:
    """Quick extraction from transcript"""
    template = load_template(form_type)
    return extract_with_citations(transcript, template, form_type)

def quick_entities(text: str) -> List[Dict]:
    """Quick entity extraction"""
    return extract_medical_entities(text)

def save_results(data: Dict, filename: str) -> str:
    """Save results to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    return filename