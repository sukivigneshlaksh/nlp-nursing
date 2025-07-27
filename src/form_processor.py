import sys
import os
from google import genai
from google.genai.types import HttpOptions, Part
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

def process_form(pdf_path, output_path, form_name="Medical Form"):
    """
    Process any medical form PDF and extract structured data as JSON.
    
    Args:
        pdf_path: Path to the PDF form
        output_path: Path to save the JSON output
        form_name: Name of the form for context
    """
    prompt = f"""
Extract data from this {form_name} and format as JSON.

Please extract the following key information sections and populate them as available:

Instructions:
- For multiple choice fields, include all applicable options
- For date fields, use MM/DD/YYYY format if dates are present
- For codes/numbers, include the actual values found in the form
- Create a structured JSON with logical sections
- If sections are not applicable or not found, leave as empty
- Use descriptive field names that match the form labels
"""

    try:
        with open(pdf_path, "rb") as f:
            pdf_data = f.read()

        print(f"Extracting {form_name} Data...")
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

        with open(output_path, "w") as f:
            f.write(response.text)

        print(f"✓ {form_name} data extracted to: {output_path}")
        return True

    except FileNotFoundError:
        print(f"Error: PDF file not found: {pdf_path}")
        return False
    except Exception as e:
        print(f"Error processing {form_name}: {e}")
        return False

def main():
    """Command line interface for form processing."""
    if len(sys.argv) < 3:
        print("Usage: python form_processor.py <pdf_path> <output_path> [form_name]")
        print("Example: python form_processor.py ../data/pdf/CMS_Form.pdf ../outputs/cms_output.json 'CMS Form'")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_path = sys.argv[2]
    form_name = sys.argv[3] if len(sys.argv) > 3 else "Medical Form"
    
    success = process_form(pdf_path, output_path, form_name)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()