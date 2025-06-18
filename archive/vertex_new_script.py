import base64
import os
import time
from pathlib import Path
import glob

import fitz  # PyMuPDF
from dotenv import load_dotenv
from openai import OpenAI
import vertexai
from vertexai.generative_models import GenerativeModel, Part

load_dotenv()

# Initialize OpenAI
openai_client = OpenAI()

# Initialize Vertex AI
project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "suki-dev")
location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
vertexai.init(project=project_id, location=location)
gemini_model = GenerativeModel("gemini-1.5-flash")

def pdf_to_images_openai(pdf_path: str) -> list[str]:
    """Convert PDF to base64 images for OpenAI"""
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img_data = pix.tobytes("png")
        images.append(base64.b64encode(img_data).decode())
    doc.close()
    return images

def pdf_to_images_vertex(pdf_path: str) -> list[bytes]:
    """Convert PDF to raw bytes for Vertex AI"""
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img_data = pix.tobytes("png")
        images.append(img_data)
    doc.close()
    return images

def extract_fields_openai(images: list[str]) -> str:
    """Extract fields using OpenAI GPT-4o"""
    content = [{"type": "text", "text": "List every fillable field in this form with its exact label and data type."}]
    for img in images:
        content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img}"}})
    
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": content}],
        max_tokens=2000
    )
    return response.choices[0].message.content

def extract_fields_vertex(images: list[bytes]) -> str:
    """Extract fields using Vertex AI Gemini"""
    prompt = "List every fillable field in this form with its exact label and data type."
    
    parts = [prompt]
    for img_data in images:
        parts.append(Part.from_data(mime_type="image/png", data=img_data))
    
    response = gemini_model.generate_content(parts)
    return response.text

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

def text_to_pydantic_with_gold(fields_text: str, model_client) -> str:
    """Generate Pydantic model WITH golden standard example"""
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

    GOLDEN STANDARD EXAMPLE:
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

    if isinstance(model_client, OpenAI):
        response = model_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )
        return clean_code_output(response.choices[0].message.content)
    else:  # Vertex AI
        response = model_client.generate_content(prompt)
        return clean_code_output(response.text)

def text_to_pydantic_without_gold(fields_text: str, model_client) -> str:
    """Generate Pydantic model WITHOUT golden standard example"""
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

    OUTPUT: Pure Python code only, no explanations or markdown.
    """

    if isinstance(model_client, OpenAI):
        response = model_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )
        return clean_code_output(response.choices[0].message.content)
    else:  # Vertex AI
        response = model_client.generate_content(prompt)
        return clean_code_output(response.text)

# Main execution
pdf_file = "pdf/CMS_Form.pdf"
pdf_name = Path(pdf_file).stem

print(f"\n{'='*60}")
print(f"PROCESSING: {pdf_file}")
print(f"{'='*60}")

# Prepare images for both models
openai_images = pdf_to_images_openai(pdf_file)
vertex_images = pdf_to_images_vertex(pdf_file)

# Extract fields once with each model
print("Extracting fields with OpenAI...")
openai_fields = extract_fields_openai(openai_images)

print("Extracting fields with Vertex AI...")
vertex_fields = extract_fields_vertex(vertex_images)

# Test configurations
configs = [
    ("openai", "with_gold", openai_client, openai_fields, text_to_pydantic_with_gold),
    ("openai", "without_gold", openai_client, openai_fields, text_to_pydantic_without_gold),
    ("vertex", "with_gold", gemini_model, vertex_fields, text_to_pydantic_with_gold),
    ("vertex", "without_gold", gemini_model, vertex_fields, text_to_pydantic_without_gold)
]

for model_name, gold_status, model_client, fields_text, generation_func in configs:
    output_dir = f"outputs/{pdf_name}/{model_name}_{gold_status}"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n--- {model_name.upper()} {gold_status.replace('_', ' ').upper()} ---")
    
    for i in range(5):
        print(f"Run {i+1}/5", end=" ")
        try:
            pydantic_code = generation_func(fields_text, model_client)
            
            with open(f"{output_dir}/model_run_{i+1}.py", "w") as f:
                f.write(pydantic_code)
            
            print("✓")
        except Exception as e:
            print(f"✗ Error: {e}")
            with open(f"{output_dir}/model_run_{i+1}_ERROR.txt", "w") as f:
                f.write(str(e))

print(f"\n{'='*60}")
print("COMPARISON COMPLETE")
print("Check outputs/ directory for results organized by:")
print("- PDF name")
print("- Model (openai/vertex)")  
print("- Gold standard (with_gold/without_gold)")
print(f"{'='*60}")