"""
Landing AI Document Extraction - Get chunks from PDF + Vertex AI disjoint analysis

Setup:
pip install agentic-doc
export VISION_AGENT_API_KEY="your-api-key"
"""

import os
import json
import sys
from pathlib import Path
from dotenv import load_dotenv
import pickle
import concurrent.futures
import threading

# Load environment variables from .env file
load_dotenv()

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

import vertexai
from vertexai.generative_models import GenerativeModel

# Initialize Vertex AI
vertexai.init(project="suki-dev", location="us-central1")
model = GenerativeModel("gemini-1.5-pro")

def extract_chunks(pdf_path: str):
    """Extract chunks from PDF."""
    from agentic_doc import parse

    result = parse.parse_documents([pdf_path])
    return result[0].chunks


def extract_chunk_images(chunks, pdf_path):
    """Extract images for each chunk from the PDF and return as byte data."""
    import fitz  # PyMuPDF
    
    # Open the PDF
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


def create_form_structure(section_data, section_id):
    """First kernel call: Create form structure for a section"""
    
    # Prepare section content for analysis
    section_text = ""
    for chunk in section_data["chunks"]:
        section_text += f"Chunk {chunk['chunk_id']}: {chunk['text']}\n"
    
    prompt = f"""
    FORM STRUCTURE CREATION - Section {section_id}
    
    Analyze this section and create a form structure template:
    
    SECTION DATA:
    {section_text}
    
    Create a JSON structure with empty fields ready for data filling:
    {{
      "section_id": {section_id},
      "section_type": "patient_demographics|medical_history|etc",
      "fields": [
        {{
          "field_name": "patient_name",
          "field_type": "text_input",
          "label": "Patient Name",
          "required": true,
          "value": null
        }},
        {{
          "field_name": "date_of_birth",
          "field_type": "date", 
          "label": "Date of Birth",
          "required": true,
          "value": null
        }}
      ]
    }}
    
    Return ONLY the JSON structure with null values ready for filling.
    """
    
    response = model.generate_content([prompt])
    
    try:
        text = response.text.strip()
        if text.startswith("```"):
            lines = text.split('\n')
            text = '\n'.join(lines[1:-1])
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "section_id": section_id,
            "section_type": "unknown",
            "fields": [],
            "error": "Structure creation failed"
        }


def fill_form_structure(form_structure, transcript):
    """Second kernel call: Fill the form structure with transcript data"""
    
    prompt = f"""
    FORM FILLING - Fill structure with transcript data
    
    FORM STRUCTURE:
    {json.dumps(form_structure, indent=2)}
    
    TRANSCRIPT:
    {transcript}
    
    TASK: Fill the "value" field for each form field using transcript data.
    
    RULES:
    - Use ONLY information explicitly stated in transcript
    - If info not available, keep value as null
    - Match field types (text, date, checkbox, etc.)
    - Use exact quotes from transcript when possible
    
    Return the same structure with filled values.
    """
    
    response = model.generate_content([prompt])
    
    try:
        text = response.text.strip()
        if text.startswith("```"):
            lines = text.split('\n')
            text = '\n'.join(lines[1:-1])
        return json.loads(text)
    except json.JSONDecodeError:
        # Return original structure with error note
        form_structure["fill_error"] = "Failed to fill form"
        return form_structure


def combined_kernel_function(section_data, section_id, transcript):
    """Combined kernel: structure creation + filling in one function"""
    
    thread_name = threading.current_thread().name
    print(f"    [{thread_name}] Processing section {section_id}...")
    
    try:
        # Step 1: Create structure (API call 1)
        print(f"    [{thread_name}] Step 1: Creating form structure...")
        form_structure = create_form_structure(section_data, section_id)
        
        # Step 2: Fill structure (API call 2) 
        print(f"    [{thread_name}] Step 2: Filling with transcript...")
        filled_form = fill_form_structure(form_structure, transcript)
        
        return {
            "section_id": section_id,
            "form_structure": form_structure,
            "filled_form": filled_form,
            "thread_id": thread_name,
            "processing_complete": True
        }
    except Exception as e:
        print(f"    [{thread_name}] Error in section {section_id}: {e}")
        return {
            "section_id": section_id,
            "error": str(e),
            "thread_id": thread_name,
            "processing_complete": False
        }


def process_sections_concurrently(sections_hashmap, transcript, max_workers=3):
    """Process all sections concurrently using ThreadPoolExecutor"""
    
    print(f"Starting concurrent processing with {max_workers} workers...")
    results = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all section processing tasks
        future_to_section = {
            executor.submit(combined_kernel_function, section_data, section_id, transcript): section_id
            for section_id, section_data in sections_hashmap.items()
        }
        
        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_section):
            section_id = future_to_section[future]
            try:
                result = future.result()
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
                    
            except Exception as e:
                print(f"❌ Section {section_id} failed: {e}")
                results[section_id] = {"section_id": section_id, "error": str(e)}
    
    return results


def find_disjoint_sections(chunks):
    """Use Vertex AI to identify disjoint sections from chunks"""
    
    # Prepare chunk data for analysis - pass full text instead of truncated
    chunks_text = []
    for i, chunk in enumerate(chunks):
        
        chunks_text.append(f"Chunk {i}: {chunk.text}")  # Remove [:200]... truncation
    
    prompt = f"""
    Analyze these document chunks and identify DISJOINT sections that can be processed independently.
    
    Disjoint means sections with completely separate information:
    - Patient Demographics (name, address, DOB)
    - Medical History (conditions, medications)
    - Current Visit (symptoms, examination)
    - Administrative Info (insurance, dates)
    
    Chunks:
    {chr(10).join(chunks_text)}
    
    Return ONLY a JSON array of CONTIGUOUS arrays with chunk indices for disjoint groups:
    [[0,1,2], [3,4], [5]]
    """
    
    response = model.generate_content([prompt])
    
    try:
        # Clean response
        text = response.text.strip()
        if text.startswith("```"):
            lines = text.split('\n')
            text = '\n'.join(lines[1:-1])
        
        disjoint_sections = json.loads(text)
        
        # Ensure contiguous sections
        contiguous_sections = []
        for section in disjoint_sections:
            sorted_section = sorted(section)
            contiguous_sections.append(sorted_section)
        
        return contiguous_sections
    except json.JSONDecodeError:
        # Fallback: each chunk is its own section
        return [[i] for i in range(len(chunks))]


def process_single_pdf(pdf_path, form_name, transcript):
    """Process a single PDF and return results"""
    print(f"Processing {form_name}...")
    
    pickle_path = f"{form_name}_chunks.pkl"
    
    # Step 1: Extract chunks
    if os.path.exists(pickle_path):
        with open(pickle_path, "rb") as f:
            chunks = pickle.load(f)
    else:
        chunks = extract_chunks(pdf_path)
        with open(pickle_path, "wb") as f:
            pickle.dump(chunks, f)
    
    # Skip image extraction
    chunk_images = {}
    
    # Step 2: Find disjoint sections
    disjoint_sections = find_disjoint_sections(chunks)
    
    # Create hashmap of disjoint sections
    sections_hashmap = {}
    
    for section_id, chunk_indices in enumerate(disjoint_sections):
        section_data = {
            "section_id": section_id,
            "chunk_indices": chunk_indices,
            "chunks": []
        }
        
        for chunk_idx in chunk_indices:
            chunk = chunks[chunk_idx]
            chunk_data = {
                "chunk_id": chunk_idx,
                "text": chunk.text,
                "chunk_type": str(chunk.chunk_type),
                "page": chunk.grounding[0].page if chunk.grounding else None
            }
            
            # Skip image file generation
            # chunk_data["image_extraction"] = "disabled"
            
            section_data["chunks"].append(chunk_data)
        
        sections_hashmap[section_id] = section_data
        print(f"  Section {section_id}: {len(chunk_indices)} chunks added to hashmap")
    
    # Step 3: Process all sections concurrently
    print(f"\nProcessing sections with concurrent kernel functions...")
    
    # Process all sections concurrently
    concurrent_results = process_sections_concurrently(sections_hashmap, transcript, max_workers=3)
    
    # Combine results with section data
    all_sections = []
    for section_id, section_data in sections_hashmap.items():
        # Add concurrent processing results
        section_data["kernel_output"] = concurrent_results.get(section_id, {"error": "No result"})
        all_sections.append(section_data)
    
    # Create final result
    result = {
        "form_name": form_name,
        "pdf_path": pdf_path,
        "total_chunks": len(chunks),
        "section_count": len(disjoint_sections),
        "sections_hashmap": sections_hashmap,
        "disjoint_sections": all_sections,
        "transcript": transcript,
        "processing_timestamp": json.dumps({"timestamp": "2025-01-15T10:00:00Z"})
    }
    
    # Save to JSON file with kernel outputs
    json_filename = f"{form_name}_processed.json"
    with open(json_filename, "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"\nSaved kernel-processed form to {json_filename}")
    print(f"Image generation disabled - no PNG files created")
    
    # Display final summary
    print(f"\nKernel Processing Summary for {form_name}:")
    print(f"Total sections processed: {len(all_sections)}")
    
    total_fields = 0
    total_filled = 0
    
    for section in all_sections:
        kernel_output = section["kernel_output"]
        form_structure = kernel_output.get("form_structure", {})
        filled_form = kernel_output.get("filled_form", {})
        
        section_id = section["section_id"]
        section_type = form_structure.get("section_type", "unknown")
        field_count = len(form_structure.get("fields", []))
        
        filled_count = 0
        for field in filled_form.get("fields", []):
            if field.get("value") is not None:
                filled_count += 1
        
        total_fields += field_count
        total_filled += filled_count
        
        print(f"  Section {section_id}: {section_type} ({filled_count}/{field_count} fields filled)")
    
    fill_rate = (total_filled / total_fields * 100) if total_fields > 0 else 0
    print(f"\nOverall: {total_filled}/{total_fields} fields filled ({fill_rate:.1f}%)")
    
    return result


if __name__ == "__main__":
    # Import transcripts
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
    
    # Process each PDF
    all_results = []
    
    for config in pdf_configs:
        try:
            result = process_single_pdf(
                pdf_path=config["path"],
                form_name=config["name"], 
                transcript=config["transcript"]
            )
            all_results.append(result)
            
        except Exception as e:
            print(f"\n❌ Error processing {config['name']}: {e}")
            continue
    
    # Create summary report
    print(f"\n{'='*60}")
    print("FINAL PROCESSING SUMMARY")
    print(f"{'='*60}")
    print(f"Total forms processed: {len(all_results)}")
    
    for result in all_results:
        form_name = result["form_name"]
        section_count = result["section_count"]
        chunk_count = result["total_chunks"]
        print(f"✅ {form_name}: {section_count} sections, {chunk_count} chunks")
    
    print(f"\nJSON files created for each form with complete processing results.")