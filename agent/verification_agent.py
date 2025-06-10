import base64
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from pydantic_ai import Agent
import fitz
from PIL import Image
import io

from vertexai.generative_models import GenerativeModel, Part
import vertexai

from utils import load_parsed_doc
from .base_agent import BaseFormAgent
import json


class ChunkSuggestions(BaseModel):
    suggestions: str = Field(..., description="Concise suggestions for improving this chunk's field extraction")


class VisionVerificationAgent(BaseFormAgent):
    def __init__(self, model: str = "gemini-1.5-flash", project_id: str = "suki-dev", location: str = "us-central1", **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.project_id = project_id
        self.location = location
        self._vision_agent = None
        self._gemini_model = None
        
        if self.is_gemini_model(model):
            try:
                vertexai.init(project=self.project_id, location=self.location)
                
                model_name = self.get_gemini_model_name(model)
                self._gemini_model = GenerativeModel(model_name)
                print(f"Initialized Vertex AI Gemini model: {model_name}")
                print(f"Project: {self.project_id}, Location: {self.location}")
            except Exception as e:
                print(f"Failed to initialize Vertex AI Gemini model: {e}")
                raise
    
    def _create_vision_agent(self) -> Agent:
        if self._vision_agent is None and not self.is_gemini_model(self.model):
            prompt = """You are a medical records specialist with 10+ years of experience reviewing healthcare forms and documents.

            Your task: Examine the PDF image and extracted fields, then output ONE of these responses:
            
            1. "No changes needed" - if extraction is accurate and well-organized
            2. Brief, specific suggestion - if you see clear improvements (max 15 words)

            Only suggest changes for clear issues:
            - Missing visible fields (e.g., "Missing 'Other' text field next to checkbox")
            - Wrong field types (e.g., "Change 'name' from radio to text")
            
            Be extremely conservative. Default to "No changes needed" unless improvement is clear."""
            
            self._vision_agent = Agent(self.model, result_type=ChunkSuggestions, system_prompt=prompt)
        
        return self._vision_agent
    
    def _extract_chunk_region(self, pdf_path: str, chunk) -> Optional[bytes]:
        if not chunk.grounding:
            print(f"  No grounding data for chunk")
            return None
        
        # Get the first grounding
        grounding = chunk.grounding[0]
        page_num = grounding.page
        box = grounding.box
        
        print(f"  Extracting region from page {page_num}")
        print(f"    Box: left={box.l:.3f}, top={box.t:.3f}, right={box.r:.3f}, bottom={box.b:.3f}")
        
        try:
            doc = fitz.open(pdf_path)
            page = doc.load_page(page_num)
            
            # Get page dimensions
            page_rect = page.rect
            print(f"    Page size: {page_rect.width} x {page_rect.height}")
            
            # Convert normalized coordinates (0-1) to actual pixel coordinates
            actual_box = fitz.Rect(
                box.l * page_rect.width,   # left
                box.t * page_rect.height,  # top
                box.r * page_rect.width,   # right
                box.b * page_rect.height   # bottom
            )
            
            # Add padding around the region
            padding = 20
            actual_box.x0 = max(0, actual_box.x0 - padding)
            actual_box.y0 = max(0, actual_box.y0 - padding)
            actual_box.x1 = min(page_rect.width, actual_box.x1 + padding)
            actual_box.y1 = min(page_rect.height, actual_box.y1 + padding)
            
            print(f"    Actual crop box: {actual_box}")
            
            # Extract the region as high-quality image
            pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72), clip=actual_box)
            img_data = pix.tobytes("png")
            
            doc.close()
            
            print(f"    Extracted region: {len(img_data):,} bytes")
            return img_data
            
        except Exception as e:
            print(f"    Error extracting region: {e}")
            return None
    
    def _analyze_chunk_with_gemini(self, chunk_data: Dict, region_img: bytes) -> str:
        try:
            # Prepare fields summary for analysis
            fields_summary = []
            for field in chunk_data["fields"]:
                field_desc = f"- {field['question']} (Type: {field['type']}"
                if field.get('options'):
                    field_desc += f", Options: {field['options']}"
                field_desc += ")"
                fields_summary.append(field_desc)
            
            fields_text = "\n".join(fields_summary)
            
            # Create prompt for vision analysis
            prompt = f"""You are a medical records specialist with 10+ years of experience reviewing healthcare forms and documents.

Analyze this PDF form region and the extracted fields below.

EXTRACTED FIELDS:
{fields_text}

Your task: Examine the PDF image and extracted fields, then output ONE of these responses:

1. "No changes needed" - if extraction is accurate and well-organized
2. Brief, specific suggestion - if you see clear improvements (max 15 words)

Only suggest changes for obvious issues:
- Conditional fields that should be merged (e.g., "Merge 'pregnant' + 'due_date' fields")
- Missing visible fields (e.g., "Missing 'Other' text field next to checkbox")  
- Wrong field types (e.g., "Change 'name' from radio to text")

Be extremely conservative. Default to "No changes needed" unless improvement is obvious.

Respond with just the suggestion text, nothing else."""
            
            # Create image part for Vertex AI
            image_part = Part.from_data(
                mime_type="image/png",
                data=region_img
            )
            
            # Generate response using Vertex AI Gemini
            response = self._gemini_model.generate_content([prompt, image_part])
            
            return response.text.strip()
            
        except Exception as e:
            print(f"  Vertex AI Gemini vision analysis error: {e}")
            return f"Vertex AI Gemini vision analysis failed: {str(e)}"
    
    def _analyze_chunk_with_vision(self, chunk_data: Dict, region_img: bytes) -> str:
        try:
            # Prepare fields summary for analysis
            fields_summary = []
            for field in chunk_data["fields"]:
                field_desc = f"- {field['question']} (Type: {field['type']}"
                if field.get('options'):
                    field_desc += f", Options: {field['options']}"
                field_desc += ")"
                fields_summary.append(field_desc)
            
            fields_text = "\n".join(fields_summary)
            
            # Create prompt for vision analysis
            img_b64 = base64.b64encode(region_img).decode()
            prompt = f"""Analyze this PDF form region and the extracted fields.

EXTRACTED FIELDS:
{fields_text}

Instructions:
- If extraction is accurate and well-organized: respond "No changes needed"  
- If you see obvious improvements: state them in 15 words or less
- Be conservative - only suggest clear, obvious changes

Examples:
- "No changes needed"
- "Merge 'pregnant' + 'due_date' into conditional field"
- "Missing 'Other' text field next to checkbox"
"""
            
            # Get vision suggestions
            vision_agent = self._create_vision_agent()
            result = vision_agent.run_sync(
                prompt,
                message_parts=[
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
                ]
            )
            
            return result.output.suggestions
            
        except Exception as e:
            print(f"  Vision analysis error: {e}")
            return f"Vision analysis failed: {str(e)}"
    
    def process(self, pdf_path: str, extraction_file: Optional[str] = None, **kwargs) -> Dict[Any, Any]:
        """
        Verify extracted form fields using vision analysis
        
        Args:
            pdf_path: Path to the original PDF file
            extraction_file: Path to extraction results (optional, will auto-detect)
            
        Returns:
            Dictionary containing verification results
        """
        print(f"=== STARTING VISION VERIFICATION ===")
        print(f"PDF: {pdf_path}")
        print(f"Using model: {self.model}")
        
        # Load extraction results
        if extraction_file is None:
            pdf_name = self.get_pdf_name(pdf_path)
            extraction_file = f"2-text_to_json_initial/{pdf_name}_simple.json"
        
        extraction_data = self.load_json(extraction_file)
        if not extraction_data:
            raise FileNotFoundError(f"Could not load extraction file: {extraction_file}")
        
        chunks_data = extraction_data['chunks']
        
        # Load parsed document
        parsed_doc = load_parsed_doc(pdf_path)
        if not parsed_doc:
            raise FileNotFoundError("No parsed document found - run extraction first")
        
        print(f"Verifying {len(chunks_data)} chunks...")
        
        # Create verified structure
        verified_data = {
            "document_metadata": extraction_data.get("document_metadata", {}),
            "chunks": {},
            "summary": extraction_data.get("summary", {})
        }
        
        # Process each chunk
        for chunk_key, chunk_data in chunks_data.items():
            chunk_index = int(chunk_key.split('_')[1])  # Extract index from 'chunk_X'
            
            print(f"\nVerifying {chunk_key} ({len(chunk_data['fields'])} fields)...")
            
            # Start with original data
            verified_chunk = {
                "chunk_type": chunk_data["chunk_type"],
                "original_fields": chunk_data["fields"],
                "vision_suggestions": "No visual analysis available"
            }
            
            # Skip if no fields to verify
            if not chunk_data["fields"]:
                verified_chunk["vision_suggestions"] = "No fields extracted - chunk appears to contain no form elements"
                verified_data["chunks"][chunk_key] = verified_chunk
                continue
            
            # Get corresponding parsed chunk
            if chunk_index < len(parsed_doc.chunks):
                chunk = parsed_doc.chunks[chunk_index]
                
                # Extract region image
                region_img = self._extract_chunk_region(pdf_path, chunk)
                if region_img:
                    # Use appropriate vision analysis method
                    if self.is_gemini_model(self.model):
                        suggestion = self._analyze_chunk_with_gemini(chunk_data, region_img)
                    else:
                        suggestion = self._analyze_chunk_with_vision(chunk_data, region_img)
                    
                    verified_chunk["vision_suggestions"] = suggestion
                    print(f"  Vision suggestion: {suggestion}")
                else:
                    verified_chunk["vision_suggestions"] = "Could not extract image region for analysis"
            else:
                verified_chunk["vision_suggestions"] = "Chunk index out of range"
            
            verified_data["chunks"][chunk_key] = verified_chunk
        
        # Save verified results
        pdf_name = self.get_pdf_name(pdf_path)
        output_file = f"3-text_to_json_verified/{pdf_name}_verified.json"
        output_path = self.save_json(verified_data, output_file)
        
        print(f"\n=== VERIFICATION COMPLETE ===")
        print(f"Chunks verified: {len(chunks_data)}")
        print(f"Results saved to: {output_path}")
        
        # Print summary of suggestions
        suggestions_count = 0
        for chunk_key, chunk_data in verified_data["chunks"].items():
            suggestion = chunk_data["vision_suggestions"]
            if (suggestion and suggestion.strip() != "No changes needed" and 
                "No visual analysis" not in suggestion and 
                "Vision analysis failed" not in suggestion and 
                "Could not extract" not in suggestion):
                suggestions_count += 1
                print(f"\n{chunk_key}: {suggestion}")
        
        print(f"\nChunks with improvement suggestions: {suggestions_count}")
        
        return verified_data