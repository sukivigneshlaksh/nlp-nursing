import os
import json
import sys
from pathlib import Path
from dotenv import load_dotenv
import pickle
from openai import OpenAI
from form_struct import DisjointSections, FormStructure
import base64

# Load environment variables from .env file
load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))


def extract_chunks(pdf_path: str):
  """Extract chunks from PDF."""
  from agentic_doc import parse

  result = parse.parse_documents([pdf_path])
  return result[0].chunks


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

def kernel_function(section_data, section_id, transcript):
  """Combined kernel: structure creation + filling in one function"""
  
  print(f"Processing section {section_id}...")
  
  try:    
      print(f"Step 2: Filling with transcript...")
      filled_form = process_form_with_openai(form_structure, transcript)
      
      return {
          "section_id": section_id,
          "filled_form": filled_form,
          "processing_complete": True
      }
  except Exception as e:
      print(f"Error in section {section_id}: {e}")
      return {
          "section_id": section_id,
          "error": str(e),
          "processing_complete": False
      }


def process_sections(sections_hashmap, transcript):
  """Process all sections sequentially"""
  
  print(f"Starting sequential processing...")
  results = {}
  
  for section_id, section_data in sections_hashmap.items():
      result = kernel_function(section_data, section_id, transcript)
      results[section_id] = result
      
      if result.get("processing_complete"):
          form_structure = result.get("form_structure", {})
          filled_form = result.get("filled_form", {})
          section_type = form_structure.get("section_type", "unknown")
          field_count = len(form_structure.get("fields", []))
          
          filled_count = 0
          for field in filled_form.get("fields", []):
              if field.get("value") is not None:
                  filled_count += 1
          
          print(f"✅ Section {section_id}: {section_type} ({filled_count}/{field_count} fields filled)")
      else:
          print(f"❌ Section {section_id}: Processing failed")
  
  return results


def find_disjoint_sections(chunks, section_model):
    """Use OpenAI to get disjoint sections from chunks"""
    chunks_text = []
    for i, chunk in enumerate(chunks):
        chunks_text.append(f"Chunk {i}: {chunk.text}")

    
    # combine with new line
    prompt = f"""
    Analyze these document chunks and identify DISJOINT sections that can be processed independently.
    
    Disjoint means sections with completely separate information:
    - Patient Demographics (name, address, DOB)
    - Medical History (conditions, medications)
    - Current Visit (symptoms, examination)
    - Administrative Info (insurance, dates)
    
    Chunks:
    {chr(10).join(chunks_text)}
    """

    response = client.responses.parse(
            model="gpt-4.1",
                input=[
            {
                "role": "system",
                "content": "You are a medical transcription assistant. Extract the disjoint pieces of patient information and fill the form."
            },
            {
                "role": "user",
                "content": f"""{prompt}"""
            }
        ],
        text_format=section_model,
        ).output_parsed
    
    return response.sections
  

def extract_chunk_images(chunks, pdf_path):
   import fitz

   pdf_doc = fitz.open(pdf_path)
   chunk_images = {}
   
   for i, chunk in enumerate(chunks):
       if chunk.grounding:
           grounding = chunk.grounding[0]
           page_num = grounding.page
           box = grounding.box
           
           # Get the page
           page = pdf_doc[page_num]
           
           # Convert normalized coordinates to absolute coordinates
           page_rect = page.rect
           abs_rect = fitz.Rect(
               box.l * page_rect.width,
               box.t * page_rect.height,
               box.r * page_rect.width,
               box.b * page_rect.height
           )
           
           # Extract the image as PNG bytes
           mat = fitz.Matrix(2, 2)  # 2x zoom for better quality
           pix = page.get_pixmap(matrix=mat, clip=abs_rect)
           img_bytes = pix.tobytes("png")
           
           chunk_images[i] = {
               "image_bytes": img_bytes,
               "width": pix.width,
               "height": pix.height
           }
   
   pdf_doc.close()
   return chunk_images


def process_section(section, chunks, pdf_path, transcript):
    """Process a section by converting chunks to images and extracting relevant form fields"""
    
    # Get the actual chunks for this section
    section_chunks = []
    for chunk_index in section:
        section_chunks.append(chunks[chunk_index])
    
    # Extract images for the chunks in this section
    chunk_images = extract_chunk_images(section_chunks, pdf_path)
    
    # Prepare messages with images
    messages = [
        {
            "role": "system",
            "content": "You are a medical transcription assistant. Extract patient information ONLY for the form fields visible in the provided document images."
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"""
                    Extract patient information ONLY for the form fields visible in these document images.
                    
                    From this medical transcript:
                    {transcript}
                    
                    IMPORTANT: 
                    - Only fill form fields that are present in the provided document images
                    - Do not extract information for fields not visible in these images
                    - If a field is visible but no matching information exists in transcript, leave value as null
                    - Use exact quotes from transcript when possible
                    """
                }
            ]
        }
    ]
    
    # Add images to the message
    for i in range(len(section_chunks)):
        if i in chunk_images:
            # Convert image bytes to base64
            image_base64 = base64.b64encode(chunk_images[i]["image_bytes"]).decode('utf-8')
            
            messages[1]["content"].append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{image_base64}",
                    "detail": "high"
                }
            })
    
    response = client.responses.parse(
        model="gpt-4o",
        input=messages,
        text_format=FormStructure,
    )
    
    return response.output_parsed

def process_single_pdf(pdf_path, form_name, transcript):
    """Process a single PDF and return results"""
    print(f"Processing {form_name}...")

    # pkl cache
    cache_dir = Path("cache")
    cache_dir.mkdir(exist_ok=True)
    pickle_path = cache_dir / f"{form_name}_chunks.pkl"

    # get cached chunk
    if os.path.exists(pickle_path):
        with open(pickle_path, "rb") as f:
            chunks = pickle.load(f)
    else:
        chunks = extract_chunks(pdf_path)
        with open(pickle_path, "wb") as f:
            pickle.dump(chunks, f)

    # Step 2: Find disjoint sections
    disjoint_sections = find_disjoint_sections(chunks, DisjointSections)

    print("\n\n\n")
    print(disjoint_sections)

    for section in disjoint_sections:
        print(process_section(section, chunks, pdf_path, transcript))

    # result = []

    # for section in disjoint_sections:
    #     # fill with transcript information
    #     result.append(process_section(section, transcript))

    # print(result)

    # Save to JSON file with kernel outputs in outputs/agentic directory
    #   outputs_dir = Path("outputs/agentic")
    #   outputs_dir.mkdir(parents=True, exist_ok=True)
    #   json_filename = outputs_dir / f"{form_name}_processed.json"
    #   with open(json_filename, "w") as f:
    #       json.dump(result, f, indent=2)

    #   return result


if __name__ == "__main__":
  from form_transcripts import SIMPLE_FORM_TRANSCRIPT, CMS_FORM_TRANSCRIPT, UHC_FORM_TRANSCRIPT, WELLNESS_FORM_TRANSCRIPT
  
  # Define PDFs and their corresponding transcripts
  pdf_configs = [
      {
          "name": "simple_form",
          "path": "../data/pdf/Simple_Form.pdf",
          "transcript": SIMPLE_FORM_TRANSCRIPT
      },
      {
          "name": "cms_form", 
          "path": "../data/pdf/CMS_Form.pdf",
          "transcript": CMS_FORM_TRANSCRIPT
      },
      {
          "name": "uhc_form",
          "path": "../data/pdf/UHC_form.pdf", 
          "transcript": UHC_FORM_TRANSCRIPT
      },
      {
          "name": "wellness_form",
          "path": "../data/pdf/Wellness_Form.pdf",
          "transcript": WELLNESS_FORM_TRANSCRIPT
      }
  ]
  
  for config in pdf_configs:
      print(process_single_pdf(config["path"], config["name"], config["transcript"]))
      break
      