"""
Simple Form Pydantic Model - Minimal viable working code
"""

from pydantic import BaseModel
from typing import Optional, List
from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Medication(BaseModel):
    medication: str
    purpose: str

class Hospitalization(BaseModel):
    hospital: str
    date_occurred: Optional[str]
    reason: str

class Surgery(BaseModel):
    surgery: str
    date_occurred: Optional[str]

class SimpleForm(BaseModel):
    name: str
    age: Optional[int]
    county_of_residence: str
    major_medical_problems: List[str]
    current_doctor: str
    current_medications: List[Medication]
    hospitalizations: List[Hospitalization]
    surgeries: List[Surgery]

def fill_simple_form_with_transcript(transcript: str) -> SimpleForm:
    response = client.responses.parse(
        model="gpt-4.1",
            input=[
        {
            "role": "system",
            "content": "You are a medical transcription assistant. Extract patient information from the transcript and fill the form."
        },
        {
            "role": "user",
            "content": f"""
            Extract patient information from this medical transcript:
            
            {transcript}
            
            Fill out the form with all available information. If information is not available, use appropriate defaults or empty lists.
            """
        }
    ],
    text_format=SimpleForm,
    )
    
    return response.output_parsed

if __name__ == "__main__":
    try:
        from form_transcripts import SIMPLE_FORM_TRANSCRIPT
        
        print("=== Simple Form Processing ===")
        
        # Fill the form
        filled_form = fill_simple_form_with_transcript(SIMPLE_FORM_TRANSCRIPT)
        
        # Display results
        print(f"Patient: {filled_form.name}")
        print(f"Age: {filled_form.age}")
        print(f"County: {filled_form.county_of_residence}")
        print(f"Doctor: {filled_form.current_doctor}")
        print(f"Medical Problems: {filled_form.major_medical_problems}")
        print(f"Medications: {len(filled_form.current_medications)}")
        print(f"Hospitalizations: {len(filled_form.hospitalizations)}")
        print(f"Surgeries: {len(filled_form.surgeries)}")
        
        print("\n✅ Simple form filled successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")