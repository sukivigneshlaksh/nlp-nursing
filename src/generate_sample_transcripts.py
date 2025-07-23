import json
import os
from google import genai
from google.genai.types import HttpOptions
import vertexai

# Setup Vertex AI
PROJECT_ID = "suki-dev"
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)
client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION, http_options=HttpOptions(api_version="v1"))

def load_json(file_path):
    """Load JSON template from file"""
    with open(file_path, 'r') as f:
        return json.load(f)

def generate_conversation(form_structure):
    """Generate medical conversation based on form structure"""
    prompt = f"""Looking at this form structure, create a medical transcript that would include information needed to fill out the form fields.

    Form structure: {json.dumps(form_structure, indent=2)}

    Make the transcript a conversation between PATIENT and NURSE in the following style:
    **NURSE:** 
    **PATIENT:**
    **NURSE:**  

    DO NOT INCLUDE ANYTHING EXCEPT THE NURSE, PATIENT CONVERSATION.
    """

    response = client.models.generate_content(model="gemini-2.5-flash", contents=[prompt])
    return response.text.strip()

def main():
    # Load templates and generate conversations
    cms_json = load_json("../outputs/cms_output.json")
    oasis_json = load_json("../outputs/oasis_output.json")
    oasis_short_json = load_json("../outputs/oasis_output_short.json")
    
    # Create output directory
    os.makedirs("../outputs/sample_scripts", exist_ok=True)
    
    # Generate and save conversations
    print("generating cms transcript...")
    cms_conversation = generate_conversation(cms_json)
    print("generating oasis transcript...")
    oasis_conversation = generate_conversation(oasis_json)
    print("generating oasis short transcript...")
    oasis_short_conversation = generate_conversation(oasis_short_json)
    
    with open("../outputs/sample_scripts/cms_sample_transcript.txt", "w") as f:
        f.write(cms_conversation)
    
    with open("../outputs/sample_scripts/oasis_sample_transcript.txt", "w") as f:
        f.write(oasis_conversation)
    
    with open("../outputs/sample_scripts/oasis_short_sample_transcript.txt", "w") as f:
        f.write(oasis_short_conversation)

if __name__ == "__main__":
    main()