import openai
import os
from pydantic import BaseModel
from typing import Optional
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

class EducationLevel(str, Enum):
    bachelors_degree = "Bachelor's degree"
    masters_degree = "Master's degree"

class EducationOccupation(BaseModel):
    highest_education_level: Optional[EducationLevel] = None
    currently_employed: Optional[bool] = None

class MedicalFormData(BaseModel):
    education_occupation: Optional[EducationOccupation] = None

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

transcript = "I have a bachelor's degree and I work full time."

response = client.responses.parse(
    model="gpt-4o",
    input=[
        {"role": "system", "content": "Extract info."},
        {"role": "user", "content": transcript}
    ],
    text_format=MedicalFormData,
)

print(response)

with open("response.json", "w") as f:
    f.write(response.output_parsed.model_dump_json(indent=2))