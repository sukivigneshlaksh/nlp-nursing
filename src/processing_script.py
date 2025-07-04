import json
import os
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from dotenv import load_dotenv

load_dotenv()

class PDFToJSON:
    def __init__(self, project_id: str = "suki-dev", location: str = "us-central1"):
        vertexai.init(project=project_id, location=location)
        self.model = GenerativeModel("gemini-1.5-pro")
    
    def pdf_to_json_schema(self, pdf_path: str) -> dict:
        """Convert PDF to JSON Schema without assumptions"""
        try:
            with open(pdf_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
            
            prompt = """Analyze this PDF form and extract ONLY the visible form fields. Do not make assumptions about data types or values.

            Instructions:
            - Identify each form field (text boxes, checkboxes, radio buttons, etc.)
            - Use the exact field labels/names from the form
            - Map to basic JSON Schema types based on field appearance:
            * Text inputs → {"type": "string"}
            * Checkboxes → {"type": "array", "items": {"type": "string"}}
            * Radio buttons → {"type": "string"}
            * Number inputs → {"type": "number"}
            - Include field descriptions using the visible labels
            - Use snake_case for property names
            - Return ONLY valid JSON Schema, no explanations

            Format:
            {
            "type": "object",
            "properties": {
                "field_name": {
                "type": "string",
                "description": "Exact label from form"
                }
            }
            }
            
            PLEASE DO A GOOD JOB MY FAMILIES' LIFE DEPENDS ON IT
            """
            
            pdf_part = Part.from_data(mime_type="application/pdf", data=pdf_bytes)
            response = self.model.generate_content([prompt, pdf_part])
            
            # Clean and parse JSON
            text = response.text.strip()
            if text.startswith("```"):
                lines = text.split('\n')
                start_idx = next((i for i, line in enumerate(lines) if line.strip().startswith('```')), 0) + 1
                end_idx = next((i for i, line in enumerate(lines[start_idx:], start_idx) if line.strip().startswith('```')), len(lines))
                text = '\n'.join(lines[start_idx:end_idx]).strip()
            
            return json.loads(text)
            
        except Exception as e:
            print(f"Error generating JSON schema: {e}")
            return {"error": str(e)}
    
    def fill_json_with_transcript(self, json_schema: dict, transcript: str) -> dict:
        """Fill JSON schema with data from transcript"""
        try:
            prompt = f"""Fill this JSON schema with data from the patient transcript.

            JSON SCHEMA:
            {json.dumps(json_schema, indent=2)}

            PATIENT TRANSCRIPT:
            {transcript}

            Instructions:
            - Use actual data from transcript when available
            - Leave fields as null if no relevant data found
            - Do not invent or assume data
            - Follow the schema's data types exactly
            - Return ONLY the filled JSON data

            Format: Return a JSON object with the filled values.
            
            PLEASE DO A GOOD JOB MY FAMILIES' LIFE DEPENDS ON IT
            """
            
            response = self.model.generate_content([prompt])
            
            # Clean and parse JSON
            text = response.text.strip()
            if text.startswith("```"):
                lines = text.split('\n')
                start_idx = next((i for i, line in enumerate(lines) if line.strip().startswith('```')), 0) + 1
                end_idx = next((i for i, line in enumerate(lines[start_idx:], start_idx) if line.strip().startswith('```')), len(lines))
                text = '\n'.join(lines[start_idx:end_idx]).strip()
            
            return json.loads(text)
            
        except Exception as e:
            print(f"Error filling JSON: {e}")
            return {"error": str(e)}

def main():
    # Initialize converter
    converter = PDFToJSON()
    
    # Sample transcript
    transcript = """
    Patient: Robert Chen, DOB: 02/08/1968
    Address: 842 Elm Street, Kansas City, Missouri 64111
    Phone: 816-555-3421
    Medicare: 123-45-6789A
    Height: 70 inches, Weight: 185 lbs, Sex: Male

    Doctor: Dr. Maria Rodriguez, Sleep Medicine
    NPI: 1234567890
    Phone: 816-555-7890

    Patient: Doctor, I'm here about my sleep study results. My wife says I stop breathing at night and I'm exhausted all the time.

    Doctor: Yes Mr. Chen, your sleep study from December 18th, 2024 shows severe obstructive sleep apnea. Your AHI is 42 events per hour. You also have hypertension which qualifies you for CPAP treatment.

    Patient: What does that mean for treatment?

    Doctor: I'm prescribing a CPAP machine, HCPCS code E0601, with humidifier E0562. This is for obstructive sleep apnea, diagnosis code 327.23. You'll need this for life - 99 months in medical terms.

    Patient: Will insurance cover it?

    Doctor: Yes, Medicare covers it. Today January 15th, 2025 is your initial face-to-face evaluation. Your sleep test was conducted at our facility-based lab. You need to use it 4+ hours per night, 70% of nights over 30 days.

    Patient: What if CPAP doesn't work?

    Doctor: We can try BiPAP if CPAP is ineffective, but we start with CPAP first. I'm referring you to MedEquip Solutions, NPI 9876543210, for home delivery.

    Patient: When do I follow up?

    Doctor: March 1st, 2025 to check your compliance and see if symptoms improved. The machine tracks your usage automatically.

        """
    
    # Step 1: Convert PDF to JSON Schema
    print("Step 1: Converting PDF to JSON Schema...")
    pdf_path = "pdf/CMS_Form.pdf"  # Replace with your PDF path
    
    if not os.path.exists(pdf_path):
        print(f"PDF file not found: {pdf_path}")
        print("Please provide a valid PDF path")
        return
    
    json_schema = converter.pdf_to_json_schema(pdf_path)
    
    # Save the schema
    with open("generated_schema.json", "w") as f:
        json.dump(json_schema, f, indent=2)
    print("✓ JSON Schema saved to generated_schema.json")
    
    # Step 2: Fill schema with transcript data
    print("\nStep 2: Filling JSON with transcript data...")
    filled_json = converter.fill_json_with_transcript(json_schema, transcript)
    
    # Save the filled JSON
    with open("filled_form.json", "w") as f:
        json.dump(filled_json, f, indent=2)
    print("✓ Filled form saved to filled_form.json")
    
    print("\n=== GENERATED JSON SCHEMA ===")
    print(json.dumps(json_schema, indent=2))
    print("\n=== FILLED JSON DATA ===")
    print(json.dumps(filled_json, indent=2))

if __name__ == "__main__":
    main()