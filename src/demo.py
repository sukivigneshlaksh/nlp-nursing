import streamlit as st
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

def extract_with_ai(transcript, form_type):
    """Extract medical data from transcript using AI."""
    prompt = f"""Extract medical data from this transcript for a {form_type} form. Return JSON only:

{transcript}"""
    
    response = client.models.generate_content(model="gemini-2.5-flash", contents=[prompt])
    text = clean_ai_response(response.text)
    return json.loads(text)

def fill_form(template, extracted_data):
    """Fill form template with extracted data using AI."""
    prompt = f"""Fill this empty form template with the extracted data. Keep the exact structure and only fill empty fields.

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

# Main UI
st.title("Medical Form Demo")

# Load form templates
cms_template = load_template("../outputs/cms_output.json")
oasis_template = load_template("../outputs/oasis_output_short.json")

# Form selection
form_type = st.radio("Choose Form:", ["CMS", "OASIS"])
normalized_form_type = "CMS" if form_type == "CMS" else "OASIS"

# Load and display transcript
sample_transcript = load_sample_transcript(normalized_form_type)
transcript = st.text_area("Medical Transcript:", value=sample_transcript, height=300)

# Process button
if st.button("Extract Data"):
    template = cms_template if form_type == "CMS" else oasis_template
    
    with st.spinner("Processing..."):
        extracted = extract_with_ai(transcript, form_type)
        filled = fill_form(template, extracted)
    
    # Compare filled vs empty
    original_fields = get_field_values(template)
    new_fields = get_field_values(filled)
    added_fields = {k: v for k, v in new_fields.items() if k not in original_fields}
    
    # Results
    st.success(f"Filled {len(added_fields)} additional fields")
    
    if added_fields:
        st.write("**Extracted Data:**")
        for field, value in sorted(added_fields.items()):
            clean_field = format_field_name(field)
            st.text(f"{clean_field}: {value}")
    
    # Side-by-side comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Empty Template")
        st.json(template, expanded=False)
    
    with col2:
        st.subheader("Populated Form")  
        st.json(filled, expanded=False)
    
    # Download option
    st.download_button(
        "Download Result",
        json.dumps(filled, indent=2),
        f"{form_type.lower().replace(' ', '_')}_filled.json"
    )