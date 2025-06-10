#!/usr/bin/env python3
"""
PDF Form Field Extraction Agent with Form Filling Capability
"""
from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pathlib import Path

from agentic_doc.parse import parse_documents
from utils import save_parsed_doc, load_parsed_doc
from .base_agent import BaseFormAgent
import json


# Pydantic models
class FormField(BaseModel):
    id: str = Field(..., description="Snake_case field identifier")
    question: str = Field(..., description="Full question text")
    type: Literal["text", "radio", "checkbox", "dropdown", "scale", "boolean"] = Field(..., description="Field type")
    options: Optional[List[str]] = Field(None, description="Available choices for radio/checkbox/dropdown")
    chunk_index: int = Field(..., description="Source chunk number")
    chunk_type: str = Field(..., description="Type of chunk this came from")


class FilledFormField(BaseModel):
    id: str = Field(..., description="Snake_case field identifier")
    question: str = Field(..., description="Full question text")
    type: Literal["text", "radio", "checkbox", "dropdown", "scale", "boolean"] = Field(..., description="Field type")
    options: Optional[List[str]] = Field(None, description="Available choices for radio/checkbox/dropdown")
    chunk_index: int = Field(..., description="Source chunk number")
    chunk_type: str = Field(..., description="Type of chunk this came from")
    filled_value: Optional[str] = Field(None, description="Value extracted from transcript")


class ChunkExtraction(BaseModel):
    fields: List[FormField] = Field(default_factory=list, description="List of form fields found")


class FormFillingResult(BaseModel):
    filled_fields: List[FilledFormField] = Field(default_factory=list, description="Fields with extracted values")


class PDFExtractionAgent(BaseFormAgent):
    def __init__(self, model: str = "openai:o4-mini", **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self._llm_agent = None
        self._form_filling_agent = None
    
    def _create_llm_agent(self) -> Agent:
        if self._llm_agent is None:
            system_prompt = """You are an expert medical form field extractor with 10+ years experience analyzing healthcare documents. 

            Your expertise:
            - Identifying form fields vs headers/instructions
            - Determining correct field types (radio, checkbox, text, boolean)  
            - Creating descriptive field IDs
            - Extracting exact answer options

            Extract ALL form fields/questions from the given chunk. Look for:
            - Questions with checkboxes, radio buttons, or text fields
            - Multiple choice options
            - Yes/No questions
            - Rating scales
            - Text input fields

            Do not extract:
            - Headers or section titles
            - Instructions or explanatory text
            - Page numbers or form metadata
            """
            
            self._llm_agent = Agent(
                self.model,
                result_type=ChunkExtraction,
                system_prompt=system_prompt
            )
        
        return self._llm_agent
    
    def _create_form_filling_agent(self) -> Agent:
        if self._form_filling_agent is None:
            system_prompt = """You are an expert medical form filling assistant with extensive experience in extracting information from clinical transcripts and medical conversations.

            Your task is to analyze a medical transcript and extract values that correspond to specific form fields. You have deep knowledge of:
            - Medical terminology and abbreviations
            - Standard medical form structures
            - Clinical conversation patterns
            - Healthcare data formats (dates, measurements, codes, etc.)

            Guidelines for filling fields:
            1. Extract EXACT values mentioned in the transcript when possible
            2. For dates: Use format mentioned in transcript or convert to MM/DD/YY if clear
            3. For radio/checkbox fields: Match transcript content to available options
            4. For numeric fields: Extract precise numbers (heights, weights, codes, etc.)
            5. For text fields: Use verbatim content when available
            6. If information is not clearly stated in transcript, leave filled_value as null
            7. Be conservative - only fill when you're confident about the information
            8. For ICD codes, HCPCS codes, etc.: Only extract if explicitly mentioned

            Do not:
            - Guess or infer information not clearly stated
            - Fill fields based on assumptions
            - Provide default values unless explicitly mentioned
            """
            
            self._form_filling_agent = Agent(
                self.model,
                result_type=FormFillingResult,
                system_prompt=system_prompt
            )
        
        return self._form_filling_agent
    
    def _process_chunk(self, chunk, chunk_index: int) -> ChunkExtraction:
        agent = self._create_llm_agent()
        
        prompt = f"""
        Analyze this chunk from a medical form and extract any form fields/questions.

        Chunk Type: {chunk.chunk_type.value}
        Chunk Index: {chunk_index}
        
        Chunk Text:
        {chunk.text}
        
        For each field found, create a descriptive ID, extract the full question text, 
        determine the field type, and list any available options.
        """

        try:
            result = agent.run_sync(prompt)
            
            # Update chunk_index and chunk_type for all fields
            extraction = result.output
            for field in extraction.fields:
                field.chunk_index = chunk_index
                field.chunk_type = chunk.chunk_type.value
                
            if extraction.fields:
                print(f"  Found {len(extraction.fields)} fields in chunk {chunk_index}")
                
            return extraction

        except Exception as e:
            print(f"Error processing chunk {chunk_index}: {e}")
            return ChunkExtraction()
    
    def _get_or_parse_document(self, pdf_path: str):
        parsed_doc = load_parsed_doc(pdf_path)
        
        if not parsed_doc:
            print(f"Parsing document: {pdf_path}")
            results = parse_documents([pdf_path])
            parsed_doc = results[0]
            save_parsed_doc(parsed_doc, pdf_path)
        else:
            print(f"Using cached parsed document: {pdf_path}")
        
        return parsed_doc
    
    def fill_form_fields(self, json_path: str, transcript_path: str) -> Dict[Any, Any]:
        """
        Fill extracted form fields using transcript content
        
        Args:
            json_path: Path to extracted form JSON (from 2-text_to_json_initial/ or 3-text_to_json_verified/)
            transcript_path: Path to transcript text file (from transcripts/)
            
        Returns:
            Enhanced JSON with filled_value added to each field
        """
        print(f"=== STARTING FORM FILLING ===")
        print(f"JSON file: {json_path}")
        print(f"Transcript: {transcript_path}")
        
        # Load the extracted form JSON
        if not Path(json_path).exists():
            # Try relative to output directory
            json_full_path = self.output_dir / json_path
            if not json_full_path.exists():
                raise FileNotFoundError(f"JSON file not found: {json_path}")
            json_path = str(json_full_path)
        
        with open(json_path, 'r', encoding='utf-8') as f:
            form_data = json.load(f)
        
        # Load the transcript
        if not Path(transcript_path).exists():
            raise FileNotFoundError(f"Transcript file not found: {transcript_path}")
        
        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript_content = f.read()
        
        print(f"Loaded transcript with {len(transcript_content)} characters")
        
        # Create form filling agent
        agent = self._create_form_filling_agent()
        
        # Process each chunk that has fields
        filled_form_data = {
            "document_metadata": form_data.get("document_metadata", {}),
            "chunks": {}
        }
        
        total_fields_processed = 0
        total_fields_filled = 0
        
        for chunk_key, chunk_data in form_data["chunks"].items():
            if not chunk_data["fields"]:
                # Copy empty chunks as-is
                filled_form_data["chunks"][chunk_key] = chunk_data
                continue
            
            print(f"Processing {chunk_key} with {len(chunk_data['fields'])} fields...")
            
            # Convert fields to FilledFormField objects for processing
            fields_to_fill = []
            for field_data in chunk_data["fields"]:
                filled_field = FilledFormField(
                    id=field_data["id"],
                    question=field_data["question"],
                    type=field_data["type"],
                    options=field_data.get("options"),
                    chunk_index=field_data["chunk_index"],
                    chunk_type=field_data["chunk_type"],
                    filled_value=None
                )
                fields_to_fill.append(filled_field)
            
            total_fields_processed += len(fields_to_fill)
            
            # Create batch prompt for this chunk's fields
            fields_info = "\n".join([
                f"- ID: {field.id}\n  Question: {field.question}\n  Type: {field.type}\n  Options: {field.options or 'N/A'}"
                for field in fields_to_fill
            ])
            
            prompt = f"""
            You are analyzing a medical transcript to fill form fields. Here are the fields from chunk {chunk_key}:

            FIELDS TO FILL:
            {fields_info}

            TRANSCRIPT CONTENT:
            {transcript_content}

            For each field, extract the appropriate value from the transcript. Be precise and conservative - only fill values that are clearly stated. Return all fields with filled_value set to the extracted value or null if not found.
            """
            
            try:
                # Process the chunk fields
                result = agent.run_sync(prompt)
                filled_fields = result.output.filled_fields
                
                # Update chunk data with filled values
                updated_fields = []
                for i, field_data in enumerate(chunk_data["fields"]):
                    # Find corresponding filled field
                    filled_field = None
                    for ff in filled_fields:
                        if ff.id == field_data["id"]:
                            filled_field = ff
                            break
                    
                    # Create updated field data
                    updated_field = field_data.copy()
                    if filled_field and filled_field.filled_value:
                        updated_field["filled_value"] = filled_field.filled_value
                        total_fields_filled += 1
                        print(f"    Filled {field_data['id']}: {filled_field.filled_value}")
                    else:
                        updated_field["filled_value"] = None
                    
                    updated_fields.append(updated_field)
                
                filled_form_data["chunks"][chunk_key] = {
                    "chunk_type": chunk_data["chunk_type"],
                    "fields": updated_fields
                }
                
            except Exception as e:
                print(f"Error filling fields for {chunk_key}: {e}")
                # Fall back to original data with null filled_values
                updated_fields = []
                for field_data in chunk_data["fields"]:
                    updated_field = field_data.copy()
                    updated_field["filled_value"] = None
                    updated_fields.append(updated_field)
                
                filled_form_data["chunks"][chunk_key] = {
                    "chunk_type": chunk_data["chunk_type"],
                    "fields": updated_fields
                }
        
        # Update summary
        filled_form_data["summary"] = {
            "total_fields": total_fields_processed,
            "fields_filled": total_fields_filled,
            "fill_rate": round(total_fields_filled / total_fields_processed * 100, 1) if total_fields_processed > 0 else 0,
            "chunks_with_fields": sum(1 for chunk_data in filled_form_data["chunks"].values() if chunk_data["fields"])
        }
        
        # Save results
        pdf_name = Path(json_path).stem.replace("_simple", "")
        
        # Save to 4-form_filled directory
        output_filename = f"4-form_filled/{pdf_name}_filled.json"
        output_path = self.save_json(filled_form_data, output_filename)
        
        print(f"\n=== FORM FILLING COMPLETE ===")
        print(f"Output: {output_path}")
        print(f"Fields processed: {total_fields_processed}")
        print(f"Fields filled: {total_fields_filled}")
        print(f"Fill rate: {filled_form_data['summary']['fill_rate']}%")
        
        return filled_form_data
    
    def process(self, pdf_path: str, **kwargs) -> Dict[Any, Any]:
        print(f"=== STARTING PDF EXTRACTION ===")
        print(f"Processing: {pdf_path}")
        
        # Get parsed document
        parsed_doc = self._get_or_parse_document(pdf_path)
        
        # Initialize result structure
        form_json = {
            "document_metadata": {
                "source_file": pdf_path,
                "total_chunks": len(parsed_doc.chunks),
            },
            "chunks": {}
        }

        print(f"Processing {len(parsed_doc.chunks)} chunks...")

        # Process each chunk
        for i, chunk in enumerate(parsed_doc.chunks):
            chunk_key = f"chunk_{i}"
            print(f"Processing {chunk_key}/{len(parsed_doc.chunks)-1}...")

            # Extract fields from chunk
            chunk_extraction = self._process_chunk(chunk, i)
            
            # Store results in chunk-keyed structure
            form_json["chunks"][chunk_key] = {
                "chunk_type": chunk.chunk_type.value,
                "fields": [field.model_dump() for field in chunk_extraction.fields]
            }
        
        # Generate summary
        total_fields = sum(len(chunk_data["fields"]) for chunk_data in form_json["chunks"].values())
        form_json["summary"] = {
            "total_fields": total_fields,
            "chunks_with_fields": sum(1 for chunk_data in form_json["chunks"].values() if chunk_data["fields"])
        }
        
        # Save results
        pdf_name = self.get_pdf_name(pdf_path)
        
        # Full results
        full_output = f"2-text_to_json_initial/{pdf_name}.json"
        full_path = self.save_json(form_json, full_output)
        
        # Simplified version
        simple_json = {
            "chunks": form_json["chunks"],
            "summary": form_json["summary"]
        }
        simple_output = f"2-text_to_json_initial/{pdf_name}_simple.json"
        simple_path = self.save_json(simple_json, simple_output)
        
        print(f"\n=== EXTRACTION COMPLETE ===")
        print(f"Full results: {full_path}")
        print(f"Simple results: {simple_path}")
        print(f"Total fields extracted: {total_fields}")
        
        return form_json