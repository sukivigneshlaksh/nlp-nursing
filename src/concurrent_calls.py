import json
import os
from typing import List, Dict
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from dotenv import load_dotenv

load_dotenv()

class ChunkGrouper:
    def __init__(self, project_id: str = "suki-dev", location: str = "us-central1"):
        vertexai.init(project=project_id, location=location)
        self.model = GenerativeModel("gemini-1.5-pro")
        
        # JSON Schema conversion prompt
        self.json_schema_prompt = """You MUST return ONLY valid JSON Schema. No explanations, no markdown, no extra text.

        Convert this medical form to JSON Schema using:
        - Checkboxes → {"type": "array", "items": {"enum": [...]}}
        - Radio buttons → {"enum": [...]}
        - Text fields → {"type": "string", "maxLength": N}
        - Numbers → {"type": "number", "minimum": X, "maximum": Y}
        - Y/N questions → {"enum": ["Y", "N", "NA"]}

        Output format:
        {
        "type": "object",
        "properties": {
            "field_name": {
            "type": "string",
            "description": "Field description"
            }
        },
        "required": []
        }

        Return ONLY the JSON object. Form section:"""
    
    def load_image_bytes(self, image_path: str) -> bytes:
        """Load image as bytes"""
        with open(image_path, "rb") as image_file:
            return image_file.read()
    
    def group_chunks(self, chunks_data: List[dict]) -> List[List[int]]:
        """Group chunks by disjoint information boundaries"""
        try:
            # Prepare content for analysis
            parts = []
            
            # Add the main prompt
            prompt = """Analyze these form chunks to identify disjoint pieces of information - where one logical section completely ends and another begins.
            Optimize for increasing the number of sections which are created while maintaining inforamtion between sections is disjoint.

            For example:
            - Personal Information section ends, Medical History begins
            - Current Medications ends, Previous Surgeries begins  
            - Contact Details ends, Insurance Information begins

            Look at both the text content and images to identify these natural boundaries.

            RETURN FORMAT: JSON array of arrays containing chunk indices
            Example: [[0,1,2], [3,4], [5,6,7,8]]
            Where each sub-array represents chunks that belong together as one complete information section.

            CHUNKS TO ANALYZE:
            """
            parts.append(prompt)
            
            # Add each chunk's content
            for i, chunk in enumerate(chunks_data):
                chunk_text = f"\nChunk {i} (ID: {chunk['chunk_id']}):\nText: {chunk['text']}\n"
                parts.append(chunk_text)
                
                # Add first image if available
                # !is there an issue with only the first image
                if chunk.get("image_paths") and len(chunk["image_paths"]) > 0:
                    image_path = chunk["image_paths"][0]
                    if os.path.exists(image_path):
                        image_bytes = self.load_image_bytes(image_path)
                        parts.append(Part.from_data(mime_type="image/png", data=image_bytes))
            
            # Add final instruction
            parts.append("\nReturn ONLY the JSON array of grouped indices:")
            
            response = self.model.generate_content(parts)

            if not response or not response.text:
                print("Error: Empty response from model")
                return [[i] for i in range(len(chunks_data))]
            
            # Parse the JSON response
            response_text = response.text.strip()
            if response_text.startswith("```"):
                response_text = response_text.split("\n", 1)[1]
                response_text = response_text.rsplit("\n", 1)[0]
            
            grouped_indices = json.loads(response_text)
            return grouped_indices
            
        except Exception as e:
            print(f"Error in grouping chunks: {e}")
            return [[i] for i in range(len(chunks_data))]

    def convert_group_to_json_schema(self, chunks_data: List[dict], group_indices: List[int]) -> dict:
        """Convert a group of chunks to JSON Schema"""
        try:
            parts = [self.json_schema_prompt]
            
            # Add combined text from all chunks in group
            combined_text = "\n\n".join([chunks_data[i]['text'] for i in group_indices])
            parts.append(f"\n\n{combined_text}")
            
            # Add images from chunks in group
            for chunk_idx in group_indices:
                chunk = chunks_data[chunk_idx]
                if chunk.get("image_paths") and len(chunk["image_paths"]) > 0:
                    image_path = chunk["image_paths"][0]
                    if os.path.exists(image_path):
                        print(f"Loading and saving image for chunk {chunk_idx}")
                        image_bytes = self.load_image_bytes(image_path)
                        
                        # Save image to output directory
                        os.makedirs("outputs_2/images", exist_ok=True)
                        output_image_path = f"outputs_2/images/chunk_{chunk_idx}_image.png"
                        with open(output_image_path, "wb") as f:
                            f.write(image_bytes)
                        
                        parts.append(Part.from_data(mime_type="image/png", data=image_bytes))
            
            response = self.model.generate_content(parts)
            response_text = response.text.strip()
            
            # Remove markdown formatting
            if response_text.startswith("```"):
                lines = response_text.split('\n')
                start_idx = next((i for i, line in enumerate(lines) if line.strip().startswith('```')), 0) + 1
                end_idx = next((i for i, line in enumerate(lines[start_idx:], start_idx) if line.strip().startswith('```')), len(lines))
                response_text = '\n'.join(lines[start_idx:end_idx]).strip()
            
            # Fix missing brackets (common Gemini bug)
            open_count = response_text.count('{')
            close_count = response_text.count('}')
            if open_count > close_count:
                response_text += '}' * (open_count - close_count)
            
            return json.loads(response_text)
            
        except Exception as e:
            print(f"Error converting group {group_indices} to JSON Schema: {e}")
            return {"error": f"Failed to convert chunks {group_indices}: {str(e)}"}

    def fill_schema_with_data(self, schema: dict, group_index: int) -> dict:
        """Fill a JSON schema with mock patient data using API call"""
        try:
            # Mock patient transcript
            transcript = """
            Patient: Robert Chen, DOB: 02/08/1968
            Address: 842 Elm Street, Kansas City, Missouri 64111
            Phone: 816-555-3421
            Medicare: 123-45-6789A
            Height: 70 inches, Weight: 185 lbs, Sex: Male

            Doctor: Dr. Maria Rodriguez, Sleep Medicine
            NPI: 1234567890
            Phone: 816-555-7890

            Patient: Doctor, I'm here about my sleep study results. My wife says I stop breathing at night and I'm exhausted all the time.

            Doctor: Yes Mr. Chen, your sleep study from December 18th, 2024 shows severe obstructive sleep apnea. Your AHI is 42 events per hour. You also have hypertension which qualifies you for CPAP treatment.

            Patient: What does that mean for treatment?

            Doctor: I'm prescribing a CPAP machine, HCPCS code E0601, with humidifier E0562. This is for obstructive sleep apnea, diagnosis code 327.23. You'll need this for life - 99 months in medical terms.

            Patient: Will insurance cover it?

            Doctor: Yes, Medicare covers it. Today January 15th, 2025 is your initial face-to-face evaluation. Your sleep test was conducted at our facility-based lab. You need to use it 4+ hours per night, 70% of nights over 30 days.

            Patient: What if CPAP doesn't work?

            Doctor: We can try BiPAP if CPAP is ineffective, but we start with CPAP first. I'm referring you to MedEquip Solutions, NPI 9876543210, for home delivery.

            Patient: When do I follow up?

            Doctor: March 1st, 2025 to check your compliance and see if symptoms improved. The machine tracks your usage automatically.
            """
            
            prompt = f"""Fill this JSON schema ONLY with data explicitly found in the patient transcript.

            SCHEMA TO FILL:
            {json.dumps(schema, indent=2)}

            PATIENT TRANSCRIPT:
            {transcript}

            Instructions:
            - Use ONLY actual data from the transcript
            - Set fields to null if data is not explicitly mentioned
            - Do NOT invent addresses, phone numbers, or costs
            - Do NOT add diagnosis codes not mentioned
            - Follow the schema's data types exactly
            - Use consistent date formats (MM/DD/YYYY)
            - Return ONLY the filled JSON data, no explanations

            Return the filled data:"""
            
            response = self.model.generate_content([prompt])
            response_text = response.text.strip()
            
            # Remove markdown formatting
            if response_text.startswith("```"):
                lines = response_text.split('\n')
                start_idx = next((i for i, line in enumerate(lines) if line.strip().startswith('```')), 0) + 1
                end_idx = next((i for i, line in enumerate(lines[start_idx:], start_idx) if line.strip().startswith('```')), len(lines))
                response_text = '\n'.join(lines[start_idx:end_idx]).strip()
            
            # Fix missing brackets
            open_count = response_text.count('{')
            close_count = response_text.count('}')
            if open_count > close_count:
                response_text += '}' * (open_count - close_count)
            
            return json.loads(response_text)
            
        except Exception as e:
            print(f"Error filling schema for group {group_index}: {e}")
            return {"error": f"Failed to fill schema: {str(e)}"}

def load_chunks_from_outputs(output_dir: str = "outputs_2") -> List[dict]:
    """Load chunks from the outputs directory"""
    chunks_path = os.path.join(output_dir, "chunks.json")
    with open(chunks_path, "r") as f:
        return json.load(f)

def main():
    # Load chunks
    chunks_data = load_chunks_from_outputs()
    print(f"Loaded {len(chunks_data)} chunks")
    
    # Initialize grouper
    grouper = ChunkGrouper()
    
    # Group chunks
    print("Analyzing chunks for disjoint information boundaries...")
    grouped_indices = grouper.group_chunks(chunks_data)
    
    # Convert each group to JSON Schema
    print("Converting groups to JSON Schema...")
    json_schemas = []
    
    for i, group in enumerate(grouped_indices):
        print(f"Converting Group {i+1}: Chunks {group}")
        schema = grouper.convert_group_to_json_schema(chunks_data, group)
        json_schemas.append({
            "group_index": i,
            "chunk_indices": group,
            "schema": schema
        })
    
    # Fill each schema with mock data
    print("Filling schemas with mock patient data...")
    filled_schemas = []
    
    for i, schema_data in enumerate(json_schemas):
        print(f"Filling Schema {i+1}")
        filled_data = grouper.fill_schema_with_data(schema_data["schema"], i)
        filled_schemas.append({
            "group_index": i,
            "chunk_indices": schema_data["chunk_indices"],
            "schema": schema_data["schema"],
            "filled_data": filled_data
        })
    
    # Save results
    output_data = {
        "grouped_indices": grouped_indices,
        "json_schemas": json_schemas,
        "filled_schemas": filled_schemas,
        "total_groups": len(grouped_indices),
        "total_chunks": len(chunks_data)
    }
    
    with open("outputs_2/json_schema_conversion.json", "w") as f:
        json.dump(output_data, f, indent=2)
    
    # Save just the filled data as a combined form
    combined_form_data = {}
    for schema in filled_schemas:
        if isinstance(schema["filled_data"], dict) and "error" not in schema["filled_data"]:
            combined_form_data.update(schema["filled_data"])
    
    with open("outputs_2/filled_form_data.json", "w") as f:
        json.dump(combined_form_data, f, indent=2)
    
    print(f"\nSaved results to outputs_2/json_schema_conversion.json")
    print(f"Saved filled form to outputs_2/filled_form_data.json")
    return output_data

if __name__ == "__main__":
    main()