#!/usr/bin/env python3
import json
import openai
from agentic_doc.parse import parse_documents

import pickle
from pathlib import Path

import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Optional, Literal


# Pydantic classes to force structure
class FormField(BaseModel):
    id: str = Field(..., description="Snake_case field identifier")
    question: str = Field(..., description="Full question text")
    type: Literal["text", "radio", "checkbox", "dropdown", "scale", "boolean"] = Field(..., description="Field type")
    options: Optional[List[str]] = Field(None, description="Available choices for radio/checkbox/dropdown")
    section: str = Field(..., description="Inferred section name")
    # Not sure if this is needed but will leave in for now
    chunk_index: int = Field(..., description="Source chunk number")
    chunk_type: str = Field(..., description="Type of chunk this came from")

class ChunkExtraction(BaseModel):
    fields: List[FormField] = Field(default_factory=list, description="List of form fields found")


#Iterative chunk processing with llm calls'
def process_chunk_with_llm(chunk, chunk_index):
        
    prompt = f"""
    Analyze this chunk from a medical form and extract any form fields/questions.
    Return ONLY valid JSON array of fields found, or empty array [] if no fields exist.

    Chunk Type: {chunk.chunk_type.value}
    Chunk Text:
    {chunk.text}

    For each field found, use this format:
    {{
      "id": "descriptive_field_name",
      "question": "Full question text",
      "type": "text|radio|checkbox|dropdown|scale|boolean",
      "options": ["array of choices if applicable"],
      "section": "inferred section name",
      "chunk_index": {chunk_index},
      "chunk_type": "{chunk.chunk_type.value}"
    }}

    Rules:
    - Only extract actual form fields/questions
    - Skip headers, footers, instructions, and metadata
    - For checkboxes use type "checkbox" 
    - For radio buttons use type "radio"
    - For Yes/No questions use type "boolean"
    - For rating scales use type "scale"
    - Use snake_case for field IDs
    - Return empty array [] if no fields found

    Return only the JSON array, no explanations:
    """
    
    try:
        # Make api request
        response = openai.chat.completions.create(
            model="gpt-4.1", # consider different versions
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        
        # CHECK THIS
        content = response.choices[0].message.content.strip()
        
        # Try to parse JSON
        fields = json.loads(content)
        
        # Ensure it's a list
        if not isinstance(fields, list):
            return []

        return fields
        
    except (json.JSONDecodeError, Exception) as e:
        print(f"Error processing chunk {chunk_index}: {e}")
        return []

# Avoids unecessary api requests
def save_parsed_doc(parsed_doc, pdf_path):
    cache_dir = Path("cache")
    cache_dir.mkdir(exist_ok=True)
    
    # Get name with .pdf
    pdf_name = Path(pdf_path).stem

    # Save within cache
    cache_file = cache_dir / f"{pdf_name}_parsed.pkl"
    
    # Saves file
    with open(cache_file, 'wb') as f:
        pickle.dump(parsed_doc, f)

def load_parsed_doc(pdf_path):
    pdf_name = Path(pdf_path).stem
    cache_file = Path("cache") / f"{pdf_name}_parsed.pkl"
    
    # Check if file exists within our cache otherwise just return None
    if cache_file.exists():
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    
    return None


def pdf_to_json(pdf_path):
    # Check if in cache
    parsed_doc = load_parsed_doc("Wellness_Form.pdf")

    # Otherwise generate code
    if not parsed_doc:
        results = parse_documents([pdf_path])
        parsed_doc = results[0]
        save_parsed_doc(parsed_doc, "Wellness_Form.pdf")

    # Initial Form
    form_json = {
        "document_metadata": {
            "source_file": pdf_path,
            "total_chunks": len(parsed_doc.chunks),
        },
        "sections": {},
        "all_fields": []
    }
    
    print(f"Processing {len(parsed_doc.chunks)} chunks...")
    
    # Iterate through chunks
    for i, chunk in enumerate(parsed_doc.chunks):
        if i == 5:
            break

        print(f"Processing chunk {i+1}/{len(parsed_doc.chunks)}...")

        # Process chunk
        chunk_fields = process_chunk_with_llm(chunk, i+1)

        
        if chunk_fields:
            print(f"  Found {len(chunk_fields)} fields in chunk {i+1}")
            
            # Add new fields
            form_json["all_fields"].extend(chunk_fields)
            
            # Add to section group
            for field in chunk_fields:
                section = field.get("section", "unknown")
                if section not in form_json["sections"]:
                    form_json["sections"][section] = []
                form_json["sections"][section].append(field)
    
    # Add summary information
    form_json["summary"] = {
        "total_fields": len(form_json["all_fields"]),
        "sections_found": len(form_json["sections"]),
        "field_types": {}
    }
    
    return form_json

def main():
    # Load key
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    pdf_path = "Wellness_Form.pdf"
    
    try:
        # Convert PDF to JSON
        result_json = pdf_to_json(pdf_path)
        # Save the complete JSON
        output_file = "wellness_form_fields.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result_json, f, indent=2, ensure_ascii=False)
        
        print(f"\n=== PROCESSING COMPLETE ===")
        print(f"Results saved to: {output_file}")
        
        # Also save a simplified version with just the fields
        simple_json = {
            "fields": result_json["all_fields"],
            "summary": result_json["summary"]
        }
        
        simple_output = "wellness_form_simple.json"
        with open(simple_output, 'w', encoding='utf-8') as f:
            json.dump(simple_json, f, indent=2, ensure_ascii=False)
        
        print(f"Simplified version saved to: {simple_output}")
        
        return result_json
    
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None
    

if __name__ == "__main__":
    main()