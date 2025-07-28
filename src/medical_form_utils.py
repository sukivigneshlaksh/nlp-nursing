import json
from google import genai
from google.genai.types import HttpOptions
import vertexai

# Configuration
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

def load_template(file_path):
    """Load JSON template from file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def clean_ai_response(text):
    """Remove markdown code blocks from AI response."""
    text = text.strip()
    if text.startswith('```'):
        text = text.split('\n', 1)[1].rsplit('\n', 1)[0]
    return text

def extract_with_citations(transcript, template, form_type):
    """Extract medical data directly into template structure with citations."""
    prompt = f"""Fill this {form_type} form template using ONLY information explicitly stated in the transcript.

TEMPLATE STRUCTURE:
{json.dumps(template, indent=2)}

TRANSCRIPT:
{transcript}

CRITICAL RULES:
- Only extract information explicitly mentioned in the conversation
- If not mentioned in transcript → leave field empty/null
- If uncertain → leave field empty/null
- For each filled field, provide the exact quote from transcript that supports it

Return JSON in this format:
{{
    "filled_form": {{ /* same structure as template with extracted values */ }},
    "citations": {{
        "field.path": {{
            "value": "extracted value",
            "source_quote": "exact text from transcript",
            "confidence": 8
        }}
    }}
}}"""
    
    response = client.models.generate_content(model="gemini-2.5-flash", contents=[prompt])
    text = clean_ai_response(response.text)
    return json.loads(text)

def fill_form(template, extracted_data):
    """Fill form template with extracted data using AI."""
    prompt = f"""Fill this empty form template with the extracted data. Keep the exact structure and only fill empty fields. DON'T INCLUDE ANYTHING NOT FOUND IN THE DATA.

    Template: {json.dumps(template)}

    Extracted data: {json.dumps(extracted_data)}

    Return only the filled JSON with the same structure."""
    
    response = client.models.generate_content(model="gemini-2.5-flash", contents=[prompt])
    text = clean_ai_response(response.text)
    return json.loads(text)

def load_sample_transcript(form_type):
    """Load and clean sample transcript based on form type."""
    file_mapping = {
        "CMS": "cms_sample_transcript.txt",
        "OASIS": "oasis_short_sample_transcript.txt"
    }
    
    file_name = file_mapping.get(form_type, "oasis_sample_transcript.txt")
    
    try:
        with open(f"../outputs/sample_scripts/{file_name}", 'r') as f:
            content = f.read()
            
        # Clean formatting
        content = content.replace("**", "").replace("*", "")
        lines = [line.strip() for line in content.split('\n') 
                if line.strip() and not line.startswith('---')]
        
        return '\n\n'.join(lines)
        
    except FileNotFoundError:
        return f"Sample {form_type} transcript not found. Please run generate_sample_transcripts.py first."

def get_field_values(obj, prefix=""):
    """Recursively extract field values from nested JSON."""
    fields = {}
    if isinstance(obj, dict):
        for key, value in obj.items():
            path = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                fields.update(get_field_values(value, path))
            elif value and str(value).strip():
                fields[path] = str(value)
    return fields

def format_field_name(field_name):
    """Clean up field names for display."""
    return field_name.replace("_", " ").replace(".", " → ").title()

def get_basic_metrics(extracted_data):
    """Calculate basic metrics without LLM."""
    field_values = get_field_values(extracted_data)
    total_fields = len(field_values)
    filled_fields = len([v for v in field_values.values() if v and str(v).strip()])
    coverage_percentage = (filled_fields / total_fields * 100) if total_fields > 0 else 0
    
    return {
        "total_fields": total_fields,
        "filled_fields": filled_fields,
        "coverage_percentage": round(coverage_percentage, 1),
        "empty_fields": total_fields - filled_fields
    }

def evaluate_citations(citation_data):
    """
    Evaluate extraction quality using existing citation data.
    
    Args:
        citation_data: Dict with 'filled_form' and 'citations' from extract_with_citations()
        
    Returns:
        Dict with metrics and field analysis
    """
    filled_form = citation_data.get("filled_form", {})
    citations = citation_data.get("citations", {})
    
    basic_metrics = get_basic_metrics(filled_form)
    
    # Convert citations to field analysis format
    field_analysis = {}
    confidence_scores = []
    
    for field_path, citation_info in citations.items():
        confidence = citation_info.get("confidence", 0)
        confidence_scores.append(confidence)
        
        field_analysis[field_path] = {
            "confidence": confidence,
            "source_quote": citation_info.get("source_quote", "No citation provided"),
            "issues": "Low confidence" if confidence < 6 else "none"
        }
    
    # Calculate overall quality
    avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
    overall_quality = round(avg_confidence)
    
    return {
        "metrics": {
            **basic_metrics,
            "overall_quality": overall_quality,
            "average_confidence": round(avg_confidence, 1)
        },
        "field_analysis": field_analysis
    }