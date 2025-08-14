"""
Simple Agentic Document Extraction
Shows progression from basic API calls to agent-based processing.
"""

import time
from typing import List, Dict
from medical_data_structures import MedicalDocument, create_empty_medical_document
from llm_api_processor import LLMAPIProcessor


class MedicalExtractionAgent:
    """Simple agent that processes medical documents with planning."""
    
    def __init__(self):
        self.processor = LLMAPIProcessor(verbose_mode=False)
        self.extraction_plan = []
    
    def create_extraction_plan(self, transcript: str) -> List[str]:
        """Create a plan for extracting data from document."""
        plan = [
            "extract_demographics",
            "extract_medications", 
            "extract_diagnoses",
            "validate_extractions"
        ]
        self.extraction_plan = plan
        return plan
    
    def execute_plan(self, transcript: str) -> MedicalDocument:
        """Execute the extraction plan step by step."""
        print("Agent creating extraction plan...")
        plan = self.create_extraction_plan(transcript)
        
        doc = create_empty_medical_document()
        doc.raw_text = transcript
        
        for step in plan:
            print(f"Agent executing: {step}")
            
            if step == "extract_demographics":
                doc.patient_demographics = self.processor.extract_patient_demographics_from_transcript(transcript)
            elif step == "extract_medications":
                doc.medications = self.processor.extract_medications_from_transcript(transcript)
            elif step == "extract_diagnoses":
                doc.diagnoses = self.processor.extract_diagnoses_from_transcript(transcript)
            elif step == "validate_extractions":
                print("Agent validating extractions...")
                time.sleep(0.1)  # Simulate validation
        
        print("Agent completed extraction plan")
        return doc


def demonstrate_agentic_extraction():
    """Show agentic vs basic extraction."""
    print("=" * 40)
    print("AGENTIC EXTRACTION DEMO")
    print("=" * 40)
    
    sample_text = "Patient John Doe, age 43. Taking Lisinopril 10mg daily. Diagnosed with hypertension."
    
    agent = MedicalExtractionAgent()
    result = agent.execute_plan(sample_text)
    
    print(f"Extracted {len(result.medications)} medications")
    print(f"Extracted {len(result.diagnoses)} diagnoses")
    
    return result


if __name__ == "__main__":
    demonstrate_agentic_extraction()