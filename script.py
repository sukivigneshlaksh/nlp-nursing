from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

class Medication(BaseModel):
   name: Optional[str] = Field(None, description="Medication name")
   purpose: Optional[str] = Field(None, description="What it's for")

class MedicalHistoryForm(BaseModel):
   name: Optional[str] = Field(None, description="Patient name")
   age: Optional[int] = Field(None, description="Patient age")
   current_doctor: Optional[str] = Field(None, description="Current doctor name")
   medical_problems: Optional[str] = Field(None, description="List of medical problems")
   medications: Optional[List[Medication]] = Field(None, description="Current medications")
   last_hospitalization: Optional[str] = Field(None, description="Most recent hospitalization")

transcript = """
Patient: Sarah Johnson, 34 years old. My current doctor is Dr. Martinez at Ohio Health.
I have hypertension and anxiety. I take Lisinopril for blood pressure and Sertraline for anxiety.
I was hospitalized at Riverside Methodist Hospital in March 2024 for chest pain evaluation.
"""

response = client.beta.chat.completions.parse(
   model="gpt-4o-2024-08-06",
   messages=[
       {"role": "system", "content": "Extract medical information from the transcript."},
       {"role": "user", "content": transcript},
   ],
   response_format=MedicalHistoryForm,
)

result = response.choices[0].message.parsed
print(result)