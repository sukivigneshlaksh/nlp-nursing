import base64
import os
import time
from pathlib import Path

import fitz  # PyMuPDF
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

def pdf_to_images(pdf_path: str) -> list[str]:
   doc = fitz.open(pdf_path)
   images = []
   for page_num in range(len(doc)):
       page = doc.load_page(page_num)
       pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
       img_data = pix.tobytes("png")
       images.append(base64.b64encode(img_data).decode())
   doc.close()
   return images

def extract_fields(images: list[str]) -> str:
   content = [{"type": "text", "text": "List every fillable field in this form with its exact label and data type."}]
   for img in images:
       content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img}"}})
   
   response = client.chat.completions.create(
       model="gpt-4o",
       messages=[{"role": "user", "content": content}],
       max_tokens=2000
   )
   return response.choices[0].message.content


def clean_code_output(response: str) -> str:
   # Remove markdown code blocks
   response = response.replace("```python", "").replace("```", "")
   
   # Remove any leading/trailing whitespace
   response = response.strip()
   
   # Remove any text before the first import
   lines = response.split('\n')
   start_idx = 0
   for i, line in enumerate(lines):
       if line.strip().startswith(('from ', 'import ')):
           start_idx = i
           break
   
   return '\n'.join(lines[start_idx:])

def text_to_pydantic(fields_text: str) -> str:
    prompt = f"""Create a Pydantic model from this form analysis:

    {fields_text}

    REQUIREMENTS:
    1. Import: Optional, List from typing; date from datetime; BaseModel, Field from pydantic
    2. Create sub-models for repeating sections (medications, hospitalizations, etc.)
    3. Use simple field names: "name" not "patient_name", "date" not "date_filled"
    4. For sub-models, use basic field names: "name", "date", "reason", "purpose"

    FIELD TYPES:
    - Text: Optional[str] = Field(None, description="...")
    - Numbers: Optional[int] = Field(None, description="...")  
    - Dates: Optional[date] = Field(None, description="...")
    - Lists: List[SubModel] = Field(default_factory=list, description="...")
    - NO Union types, NO string alternatives for dates/numbers

    NAMING STANDARDS:
    - Main fields: name, age, date, county_of_residence, major_medical_problems, current_doctor
    - Sub-model fields: name, date, purpose, reason, hospital, procedure
    - Class names: descriptive (e.g., MedicalHistoryForm, Medication, Hospitalization)

    EXAMPLE GOLDEN STANDARD OUTPUT:
    from pydantic import BaseModel, Field
    from typing import Optional, List
    from datetime import date

    class Medication(BaseModel):
        name: Optional[str] = Field(None, description="Medication name")
        purpose: Optional[str] = Field(None, description="Purpose/reason for medication")

    class Hospitalization(BaseModel):
        hospital: Optional[str] = Field(None, description="Hospital name")
        date: Optional[date] = Field(None, description="Date of hospitalization")
        reason: Optional[str] = Field(None, description="Reason for hospitalization")

    class Surgery(BaseModel):
        procedure: Optional[str] = Field(None, description="Surgery/procedure performed")
        date: Optional[date] = Field(None, description="Date of surgery")

    class MedicalHistoryForm(BaseModel):
        name: Optional[str] = Field(None, description="Patient full name")
        age: Optional[int] = Field(None, description="Patient age")
        date: Optional[date] = Field(None, description="Form completion date")
        county_of_residence: Optional[str] = Field(None, description="County where patient resides")
        major_medical_problems: Optional[str] = Field(None, description="List of major medical problems")
        current_doctor: Optional[str] = Field(None, description="Current primary care physician")
        current_medications: List[Medication] = Field(default_factory=list, description="List of current medications and their purposes")
        hospitalizations: List[Hospitalization] = Field(default_factory=list, description="Recent hospitalizations (most recent first)")
        surgeries: List[Surgery] = Field(default_factory=list, description="Recent surgeries (most recent first)")

    OUTPUT: Pure Python code only, no explanations or markdown. Follow the exact patterns shown above.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000
    )
    return clean_code_output(response.choices[0].message.content)



pdf_path = "pdf/CMS_Form.pdf"
images = pdf_to_images(pdf_path)

for i in range(20):
   print(f"\n=== RUN {i+1} ===")
   fields = extract_fields(images)
   pydantic_code = text_to_pydantic(fields)
   
   with open(f"model_run_{i+1}.py", "w") as f:
       f.write(pydantic_code)
   
   print(f"Saved to model_run_{i+1}.py")
   print("Preview:")
   print(pydantic_code[:200] + "...")