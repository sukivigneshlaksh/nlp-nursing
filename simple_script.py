from openai import OpenAI
from pydantic import BaseModel
from typing import Optional, List
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

class Medication(BaseModel):
  name: Optional[str] = Field(None, description="Medication name")
  purpose: Optional[str] = Field(None, description="Purpose for medication")

class Hospitalization(BaseModel):
  hospital: Optional[str] = Field(None, description="Hospital name")
  date: Optional[str] = Field(None, description="Date")
  reason: Optional[str] = Field(None, description="Reason for hospitalization")

class Surgery(BaseModel):
  procedure: Optional[str] = Field(None, description="Surgery description")
  date: Optional[str] = Field(None, description="Date of surgery")

class MedicalHistoryForm(BaseModel):
  name: Optional[str] = Field(None, description="Patient name")
  age: Optional[int] = Field(None, description="Patient age")
  date: Optional[str] = Field(None, description="Form completion date")
  county_of_residence: Optional[str] = Field(None, description="County of residence")
  major_medical_problems: Optional[str] = Field(None, description="List of major medical problems")
  current_doctor: Optional[str] = Field(None, description="Current doctor name")
  medications: Optional[List[Medication]] = Field(None, description="Current medications")
  hospitalizations: Optional[List[Hospitalization]] = Field(None, description="Recent hospitalizations")
  surgeries: Optional[List[Surgery]] = Field(None, description="Recent surgeries")

response = client.responses.parse(
   model="gpt-4o-2024-08-06",
   input=[
      {
          "role": "system",
          "content": "You are an expert medical information extraction specialist. Extract patient information from medical transcripts and fill out the medical history form completely.",
      },
      {"role": "user", "content": "Patient: Sarah Johnson, 34 years old, from Franklin County. Today is March 15, 2024. I'm here for my annual checkup. My current doctor is Dr. Martinez at Ohio Health. For medical problems, I have hypertension and anxiety. I take Lisinopril 10mg daily for my blood pressure and Sertraline 50mg for anxiety management. I was hospitalized at Riverside Methodist Hospital in March 2024 for chest pain evaluation, but it turned out to be nothing serious. I had my gallbladder removed at Grant Medical Center in August 2023 - that's my only surgery. I also take a multivitamin daily for general health."},
  ],
   text_format=MedicalHistoryForm,
)

result = response.output_parsed

print(result)