"""
Comprehensive Form Processing - All 4 Forms with Pydantic Models
Imports models from models.py and processes all forms with OpenAI structured output
"""

from openai import OpenAI
import os
from models import (
    MedicalHistory, 
    CMSPAPDeviceForm, 
    PriorAuthorizationRequest, 
    MedicareWellnessAssessment
)
from form_transcripts import (
    SIMPLE_FORM_TRANSCRIPT,
    CMS_FORM_TRANSCRIPT, 
    PRIOR_AUTH_TRANSCRIPT,
    WELLNESS_FORM_TRANSCRIPT
)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def process_form_with_openai(transcript, form_model):
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
    text_format=form_model,
    )
    
    return response.output_parsed

