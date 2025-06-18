from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from dotenv import load_dotenv
import time
import json

load_dotenv()
client = OpenAI()

class Medication(BaseModel):
    name: Optional[str] = Field(None, description="Name of medication")
    purpose: Optional[str] = Field(None, description="What it's for")

class Hospitalization(BaseModel):
    hospital: Optional[str] = Field(None, description="Hospital name")
    date: Optional[str] = Field(None, description="Date of hospitalization")
    reason: Optional[str] = Field(None, description="Reason for hospitalization")

class Surgery(BaseModel):
    procedure: Optional[str] = Field(None, description="Surgery/procedure name")
    date: Optional[str] = Field(None, description="Date of surgery")

class MedicalHistoryForm(BaseModel):
    name: Optional[str] = Field(None, description="Patient name")
    age: Optional[int] = Field(None, description="Patient age")
    date: Optional[str] = Field(None, description="Date form was filled")
    county_of_residence: Optional[str] = Field(None, description="County of residence")
    major_medical_problems: Optional[str] = Field(None, description="List of major medical problems")
    current_doctor: Optional[str] = Field(None, description="Current doctor name")
    medications: Optional[List[Medication]] = Field(None, description="Current medications list")
    hospitalizations: Optional[List[Hospitalization]] = Field(None, description="Recent hospitalizations (recent to earliest)")
    surgeries: Optional[List[Surgery]] = Field(None, description="Surgeries (recent to earliest)")

transcript = """
Dr. Martinez: What's your full name and age?
Patient: Michael James Thompson, 52 years old.
Dr. Martinez: Where do you live?
Patient: I live in Delaware County, Ohio.
Dr. Martinez: Tell me about your main medical problems.
Patient: I have Type 2 diabetes, high blood pressure, and chronic back pain.
Dr. Martinez: Who's your current doctor?
Patient: Dr. Amanda Chen at Ohio Health Primary Care.
Dr. Martinez: What medications are you taking?
Patient: I take Metformin 500mg twice daily for diabetes, Lisinopril 10mg daily for blood pressure, and Ibuprofen 600mg as needed for back pain.
Dr. Martinez: Any recent hospitalizations?
Patient: I was hospitalized at Riverside Methodist Hospital in January 2025 for diabetic ketoacidosis, and in September 2023 for chest pain.
Dr. Martinez: Have you had any surgeries?
Patient: I had knee surgery in June 2024 at Columbus Orthopedic Surgery Center for torn meniscus, gallbladder removal in March 2022 at Grant Medical Center, and colonoscopy in November 2023.
"""

start_time = time.time()

response = client.responses.parse(
    model="gpt-4o-2024-08-06",
    input=[
        {"role": "system", "content": "Extract the medical information."},
        {
            "role": "user",
            "content": transcript,
        },
    ],
    text_format=MedicalHistoryForm,
)


end_time = time.time()
execution_time = end_time - start_time

result = response.output_parsed

output_data = {
    "execution_time_seconds": execution_time,
    "extracted_medical_data": result.model_dump()
}

# Save to JSON file
with open("medical_extraction_results.json", "w") as f:
    json.dump(output_data, f, indent=2)

print(f"Results saved to medical_extraction_results.json")