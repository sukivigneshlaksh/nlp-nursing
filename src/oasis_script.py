import subprocess
from google import genai
from google.genai.types import HttpOptions, Part
import vertexai

# Configuration
PROJECT_ID = "suki-dev"
LOCATION = "us-central1"

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Create Vertex AI client
client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION,
    http_options=HttpOptions(api_version="v1")
)

# Create the prompt specifically for OASIS-E1 form extraction
prompt = """
Extract data from this OASIS-E1 (Outcome and Assessment Information Set) home health assessment form and format as JSON.

Please extract the following key information sections and populate them as available:

Instructions:
- For multiple choice fields, include all applicable options
- For date fields, use MM/DD/YYYY format if dates are present
- For codes/numbers, include the actual values found in the form
- If sections are not applicable or not found, leave as empty
"""

# Add this to read a PDF file:
with open("../data/pdf/Oasis_Form.pdf", "rb") as f:
    pdf_data = f.read()

print("Extracting OASIS-E1 Form Data:")
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

with open("../outputs/oasis_output.json", "w") as f:
    f.write(response.text)

print("Extracted data: \n")
print(response.text)