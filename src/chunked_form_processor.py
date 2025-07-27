import json
import PyPDF2
from google import genai
from google.genai.types import HttpOptions, Part
import vertexai
from io import BytesIO

# Configuration
PROJECT_ID = "suki-dev"
LOCATION = "us-central1"

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)
client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

def split_pdf(pdf_path, pages_per_chunk=100):
    """Split PDF into chunks."""
    chunks = []
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        total_pages = len(reader.pages)
        
        for start in range(0, total_pages, pages_per_chunk):
            end = min(start + pages_per_chunk, total_pages)
            
            writer = PyPDF2.PdfWriter()
            for page_num in range(start, end):
                writer.add_page(reader.pages[page_num])
            
            chunk_buffer = BytesIO()
            writer.write(chunk_buffer)
            chunks.append(chunk_buffer.getvalue())
            chunk_buffer.close()
    
    return chunks

def process_chunk(chunk_data, chunk_index):
    """Process PDF chunk with Vertex AI."""
    # Change this to have oasis_output json and see overlap in questions
    prompt = """Extract key data from this medical form chunk. Return valid JSON only.
    Use this exact format:
    {"section": "section_name", "fields": {"field1": "value1", "field2": ["option1", "option2"]}}
    
    Rules:
    - Use double quotes for all strings
    - Escape any quotes in values with \"
    - Only include filled fields, not empty ones
    - Keep values concise"""
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=[prompt, Part.from_bytes(data=chunk_data, mime_type="application/pdf")]
        )
        
        text = response.text.strip()
        if text.startswith('```json'):
            text = text[7:]  # Remove ```json
        elif text.startswith('```'):
            text = text[3:]   # Remove ```
        if text.endswith('```'):
            text = text[:-3]  # Remove closing ```
        text = text.strip()
        
        # Try to parse JSON, if it fails return a simple error structure
        try:
            return json.loads(text)
        except json.JSONDecodeError as json_err:
            print(f"JSON parse error in chunk {chunk_index}: {str(json_err)[:100]}")
            return {"chunk_index": chunk_index, "raw_text": text[:200], "error": "json_parse_failed"}
        
    except Exception as e:
        print(f"Error in chunk {chunk_index}: {str(e)[:100]}")
        return {"chunk_index": chunk_index, "error": "failed"}

def process_large_form(pdf_path, output_path):
    """Process large form in chunks and merge results."""
    print(f"Processing {pdf_path}...")
    
    # Split into chunks
    chunks = split_pdf(pdf_path)
    print(f"Split into {len(chunks)} chunks")
    
    # Process each chunk
    global_result = {}
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}")
        chunk_result = process_chunk(chunk, i)
        
        # Merge into global result
        if isinstance(chunk_result, dict):
            for key, value in chunk_result.items():
                if key in global_result:
                    if isinstance(global_result[key], list):
                        global_result[key].extend(value if isinstance(value, list) else [value])
                    else:
                        global_result[key] = [global_result[key], value]
                else:
                    global_result[key] = value
        else:
            # If chunk_result is not a dict, store it with chunk index
            global_result[f"chunk_{i}"] = chunk_result
    
    # Save results
    with open(output_path, 'w') as f:
        json.dump(global_result, f, indent=2)
    
    print(f"Complete. Saved to {output_path}")
    return global_result

if __name__ == "__main__":
    process_large_form("../data/pdf/Long_Form.pdf", "../outputs/long_form_chunked_output.json")