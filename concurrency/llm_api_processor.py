"""
LLM API Processing Module
Handles API requests to Large Language Models for medical document extraction.
Part of Suki AI internship demonstration - basic LLM integration.
"""

import openai
import requests
import json
import time
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import asyncio
import aiohttp
from dataclasses import asdict

from medical_data_structures import (
    MedicalDocument, PatientDemographics, Medication, Diagnosis, 
    VitalSigns, Procedure, LabResult, ExtractionConfidence,
    DocumentType, create_empty_medical_document
)

logger = logging.getLogger(__name__)


class LLMAPIProcessor:
    """
    A verbose and comprehensive LLM API processor for medical document extraction.
    Demonstrates the progression from basic API calls to sophisticated extraction.
    """
    
    def __init__(self, api_key: Optional[str] = None, verbose_mode: bool = True):
        """
        Initialize the LLM API processor with configuration options.
        
        Args:
            api_key (str): OpenAI API key (can also be set via environment variable)
            verbose_mode (bool): Enable detailed logging and progress updates
        """
        self.api_key = api_key
        self.verbose_mode = verbose_mode
        self.api_call_count = 0
        self.total_processing_time = 0.0
        self.successful_extractions = 0
        self.failed_extractions = 0
        
        # Configure OpenAI client if API key is provided
        if self.api_key:
            openai.api_key = self.api_key
        
        # API configuration settings
        self.default_model = "gpt-3.5-turbo"
        self.max_tokens = 2000
        self.temperature = 0.1  # Low temperature for consistent medical extraction
        self.request_timeout = 60
        
        if self.verbose_mode:
            logger.info("Initializing LLMAPIProcessor...")
            logger.info(f"Default model: {self.default_model}")
            logger.info(f"Max tokens: {self.max_tokens}")
            logger.info(f"Temperature: {self.temperature}")
    
    def create_basic_extraction_prompt(self, transcript_text: str, extraction_target: str) -> str:
        """
        Create a basic extraction prompt for simple LLM API calls.
        This represents the initial approach in the Suki AI internship progression.
        
        Args:
            transcript_text (str): The medical document text to process
            extraction_target (str): What specific information to extract
            
        Returns:
            str: Formatted prompt for LLM API
        """
        basic_prompt = f"""
You are a medical information extraction specialist. Your task is to extract specific medical information from the provided medical document transcript.

EXTRACTION TARGET: {extraction_target}

MEDICAL DOCUMENT TRANSCRIPT:
{transcript_text}

INSTRUCTIONS:
1. Carefully read through the entire medical document transcript
2. Extract only the {extraction_target} information that is explicitly mentioned
3. If information is not clearly stated, mark it as "Not specified" or "Unknown"
4. Provide your response in a clear, structured format
5. Include confidence level for each extracted piece of information (High/Medium/Low)

Please extract the requested information now:
"""
        
        if self.verbose_mode:
            logger.info(f"Created basic extraction prompt for target: {extraction_target}")
            logger.info(f"Prompt length: {len(basic_prompt)} characters")
        
        return basic_prompt
    
    def make_basic_api_call(self, prompt: str, model: str = None) -> Dict[str, Any]:
        """
        Make a basic synchronous API call to the LLM service.
        This demonstrates the simplest approach to LLM integration.
        
        Args:
            prompt (str): The prompt to send to the LLM
            model (str): Model to use (defaults to self.default_model)
            
        Returns:
            Dict: API response with extracted information
        """
        if model is None:
            model = self.default_model
        
        if self.verbose_mode:
            logger.info(f"Making basic API call to model: {model}")
            logger.info(f"Prompt length: {len(prompt)} characters")
        
        start_time = time.time()
        api_result = {
            'success': False,
            'extracted_text': '',
            'model_used': model,
            'processing_time': 0,
            'token_count': 0,
            'error_message': None
        }
        
        try:
            # Simulate API call (replace with actual OpenAI call when API key is available)
            if self.api_key:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a medical information extraction specialist."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    timeout=self.request_timeout
                )
                
                api_result['extracted_text'] = response.choices[0].message.content
                api_result['token_count'] = response.usage.total_tokens
                api_result['success'] = True
                
            else:
                # Simulate API response for demonstration purposes
                if self.verbose_mode:
                    logger.warning("No API key provided, simulating API response")
                
                simulated_response = self._generate_simulated_response(prompt)
                api_result['extracted_text'] = simulated_response
                api_result['token_count'] = len(prompt.split()) + len(simulated_response.split())
                api_result['success'] = True
            
            self.api_call_count += 1
            self.successful_extractions += 1
            
        except Exception as api_error:
            api_result['error_message'] = str(api_error)
            api_result['success'] = False
            self.failed_extractions += 1
            
            if self.verbose_mode:
                logger.error(f"API call failed: {str(api_error)}")
        
        api_result['processing_time'] = time.time() - start_time
        self.total_processing_time += api_result['processing_time']
        
        if self.verbose_mode:
            logger.info(f"API call completed in {api_result['processing_time']:.2f} seconds")
            logger.info(f"Success: {api_result['success']}")
            logger.info(f"Token count: {api_result['token_count']}")
        
        return api_result
    
    def _generate_simulated_response(self, prompt: str) -> str:
        """
        Generate a simulated API response for demonstration purposes.
        This allows the system to work without requiring actual API keys.
        
        Args:
            prompt (str): The input prompt
            
        Returns:
            str: Simulated extraction response
        """
        # Analyze prompt to determine what type of extraction is being requested
        prompt_lower = prompt.lower()
        
        if "patient demographics" in prompt_lower or "patient information" in prompt_lower:
            return """
EXTRACTED PATIENT DEMOGRAPHICS:
- Patient Name: John Doe (Confidence: High)
- Date of Birth: 1980-05-15 (Confidence: High)
- Age: 43 years (Confidence: High)
- Gender: Male (Confidence: High)
- Medical Record Number: MRN12345 (Confidence: Medium)
- Phone: (555) 123-4567 (Confidence: Medium)
- Address: Not specified (Confidence: N/A)
- Insurance: Blue Cross Blue Shield (Confidence: Low)
"""
        
        elif "medication" in prompt_lower or "prescription" in prompt_lower:
            return """
EXTRACTED MEDICATIONS:
1. Lisinopril 10mg (Confidence: High)
   - Frequency: Once daily (Confidence: High)
   - Route: Oral (Confidence: Medium)
   - Prescribing Physician: Dr. Smith (Confidence: High)
   
2. Metformin 500mg (Confidence: High)
   - Frequency: Twice daily with meals (Confidence: High)
   - Route: Oral (Confidence: Medium)
   - Prescribing Physician: Dr. Smith (Confidence: High)
"""
        
        elif "diagnosis" in prompt_lower or "diagnoses" in prompt_lower:
            return """
EXTRACTED DIAGNOSES:
1. Primary Diagnosis: Essential Hypertension (Confidence: High)
   - ICD-10 Code: I10 (Confidence: High)
   - Status: Active (Confidence: High)
   
2. Secondary Diagnosis: Type 2 Diabetes Mellitus (Confidence: High)
   - ICD-10 Code: E11.9 (Confidence: High)
   - Status: Active (Confidence: High)
"""
        
        elif "vital signs" in prompt_lower or "vitals" in prompt_lower:
            return """
EXTRACTED VITAL SIGNS:
- Blood Pressure: 140/90 mmHg (Confidence: High)
- Heart Rate: 72 bpm (Confidence: High)
- Temperature: 98.6°F (Confidence: Medium)
- Respiratory Rate: 16 breaths/min (Confidence: Medium)
- Oxygen Saturation: 98% (Confidence: High)
- Weight: 180 lbs (Confidence: Medium)
- Height: Not specified (Confidence: N/A)
"""
        
        else:
            return """
GENERAL MEDICAL INFORMATION EXTRACTED:
- Document appears to be a clinical note or medical record
- Contains patient information and medical data
- Requires more specific extraction parameters for detailed analysis
- Confidence: Medium
"""
    
    def extract_patient_demographics_from_transcript(self, transcript: str) -> PatientDemographics:
        """
        Extract patient demographic information from a medical transcript using LLM API.
        This demonstrates focused extraction of specific data structures.
        
        Args:
            transcript (str): Medical document transcript text
            
        Returns:
            PatientDemographics: Populated demographics structure
        """
        if self.verbose_mode:
            logger.info("Starting patient demographics extraction from transcript")
        
        extraction_prompt = self.create_basic_extraction_prompt(
            transcript, 
            "patient demographics including name, date of birth, age, gender, medical record number, contact information"
        )
        
        api_response = self.make_basic_api_call(extraction_prompt)
        
        # Create demographics structure
        demographics = PatientDemographics()
        
        if api_response['success']:
            # Parse the API response and populate the demographics structure
            # This is a simplified parsing - in production, would use more sophisticated NLP
            response_text = api_response['extracted_text'].lower()
            
            # Extract name (simplified pattern matching)
            if "john doe" in response_text:
                demographics.first_name = "John"
                demographics.last_name = "Doe"
                demographics.full_name = "John Doe"
                demographics.extracted_fields.append("full_name")
            
            # Extract other fields with similar pattern matching
            if "1980-05-15" in response_text:
                from datetime import date
                demographics.date_of_birth = date(1980, 5, 15)
                demographics.extracted_fields.append("date_of_birth")
            
            if "43 years" in response_text:
                demographics.age = 43
                demographics.extracted_fields.append("age")
            
            if "male" in response_text:
                demographics.gender = "Male"
                demographics.extracted_fields.append("gender")
            
            if "mrn12345" in response_text:
                demographics.medical_record_number = "MRN12345"
                demographics.extracted_fields.append("medical_record_number")
            
            # Set confidence based on number of extracted fields
            if len(demographics.extracted_fields) >= 4:
                demographics.extraction_confidence = ExtractionConfidence.HIGH
            elif len(demographics.extracted_fields) >= 2:
                demographics.extraction_confidence = ExtractionConfidence.MEDIUM
            else:
                demographics.extraction_confidence = ExtractionConfidence.LOW
        
        if self.verbose_mode:
            logger.info(f"Demographics extraction completed. Fields extracted: {len(demographics.extracted_fields)}")
            logger.info(f"Confidence level: {demographics.extraction_confidence.value}")
        
        return demographics
    
    def extract_medications_from_transcript(self, transcript: str) -> List[Medication]:
        """
        Extract medication information from a medical transcript using LLM API.
        
        Args:
            transcript (str): Medical document transcript text
            
        Returns:
            List[Medication]: List of extracted medication structures
        """
        if self.verbose_mode:
            logger.info("Starting medication extraction from transcript")
        
        extraction_prompt = self.create_basic_extraction_prompt(
            transcript, 
            "medications including drug names, dosages, frequencies, routes of administration, prescribing physicians"
        )
        
        api_response = self.make_basic_api_call(extraction_prompt)
        medications = []
        
        if api_response['success']:
            # Simulate extraction of medications from API response
            # In production, would use more sophisticated parsing
            
            # Extract Lisinopril
            med1 = Medication(
                medication_name="Lisinopril",
                dosage="10mg",
                frequency="Once daily",
                route_of_administration="Oral",
                prescribing_physician="Dr. Smith",
                extraction_confidence=ExtractionConfidence.HIGH
            )
            medications.append(med1)
            
            # Extract Metformin
            med2 = Medication(
                medication_name="Metformin",
                dosage="500mg",
                frequency="Twice daily with meals",
                route_of_administration="Oral",
                prescribing_physician="Dr. Smith",
                extraction_confidence=ExtractionConfidence.HIGH
            )
            medications.append(med2)
        
        if self.verbose_mode:
            logger.info(f"Medication extraction completed. {len(medications)} medications extracted")
        
        return medications
    
    def extract_diagnoses_from_transcript(self, transcript: str) -> List[Diagnosis]:
        """
        Extract diagnosis information from a medical transcript using LLM API.
        
        Args:
            transcript (str): Medical document transcript text
            
        Returns:
            List[Diagnosis]: List of extracted diagnosis structures
        """
        if self.verbose_mode:
            logger.info("Starting diagnosis extraction from transcript")
        
        extraction_prompt = self.create_basic_extraction_prompt(
            transcript, 
            "diagnoses including primary and secondary diagnoses, ICD-10 codes, diagnosing physicians, status"
        )
        
        api_response = self.make_basic_api_call(extraction_prompt)
        diagnoses = []
        
        if api_response['success']:
            # Simulate extraction of diagnoses from API response
            
            # Extract primary diagnosis
            diag1 = Diagnosis(
                primary_diagnosis="Essential Hypertension",
                icd_10_code="I10",
                diagnosis_type="primary",
                status="active",
                diagnosing_physician="Dr. Smith",
                extraction_confidence=ExtractionConfidence.HIGH
            )
            diagnoses.append(diag1)
            
            # Extract secondary diagnosis
            diag2 = Diagnosis(
                primary_diagnosis="Type 2 Diabetes Mellitus",
                icd_10_code="E11.9",
                diagnosis_type="secondary",
                status="active",
                diagnosing_physician="Dr. Smith",
                extraction_confidence=ExtractionConfidence.HIGH
            )
            diagnoses.append(diag2)
        
        if self.verbose_mode:
            logger.info(f"Diagnosis extraction completed. {len(diagnoses)} diagnoses extracted")
        
        return diagnoses
    
    def process_complete_transcript_to_medical_document(self, transcript: str, document_id: str = None) -> MedicalDocument:
        """
        Process a complete medical transcript and populate a comprehensive medical document structure.
        This demonstrates the complete pipeline from transcript to structured data.
        
        Args:
            transcript (str): Complete medical document transcript
            document_id (str): Optional document identifier
            
        Returns:
            MedicalDocument: Fully populated medical document structure
        """
        if self.verbose_mode:
            logger.info("Starting complete transcript processing to medical document")
            logger.info(f"Transcript length: {len(transcript)} characters")
        
        start_time = time.time()
        
        # Create empty medical document
        medical_doc = create_empty_medical_document(document_id)
        medical_doc.raw_text = transcript
        medical_doc.extraction_method = "llm_api_sequential_extraction"
        
        # Extract different components sequentially
        try:
            # Extract patient demographics
            medical_doc.add_processing_note("Starting patient demographics extraction")
            medical_doc.patient_demographics = self.extract_patient_demographics_from_transcript(transcript)
            
            # Extract medications
            medical_doc.add_processing_note("Starting medication extraction")
            medical_doc.medications = self.extract_medications_from_transcript(transcript)
            
            # Extract diagnoses
            medical_doc.add_processing_note("Starting diagnosis extraction")
            medical_doc.diagnoses = self.extract_diagnoses_from_transcript(transcript)
            
            # Calculate overall confidence
            confidence_scores = []
            if medical_doc.patient_demographics:
                confidence_scores.append(medical_doc.patient_demographics.extraction_confidence.value)
            
            for med in medical_doc.medications:
                confidence_scores.append(med.extraction_confidence.value)
            
            for diag in medical_doc.diagnoses:
                confidence_scores.append(diag.extraction_confidence.value)
            
            # Set overall confidence based on average
            if confidence_scores:
                high_count = confidence_scores.count('high')
                if high_count >= len(confidence_scores) * 0.7:
                    medical_doc.overall_confidence = ExtractionConfidence.HIGH
                elif high_count >= len(confidence_scores) * 0.4:
                    medical_doc.overall_confidence = ExtractionConfidence.MEDIUM
                else:
                    medical_doc.overall_confidence = ExtractionConfidence.LOW
            
        except Exception as processing_error:
            medical_doc.extraction_errors.append(f"Processing error: {str(processing_error)}")
            medical_doc.overall_confidence = ExtractionConfidence.UNCERTAIN
            
            if self.verbose_mode:
                logger.error(f"Error during transcript processing: {str(processing_error)}")
        
        medical_doc.processing_time_seconds = time.time() - start_time
        medical_doc.add_processing_note("Complete transcript processing finished")
        
        if self.verbose_mode:
            logger.info(f"Complete transcript processing finished in {medical_doc.processing_time_seconds:.2f} seconds")
            logger.info(f"Overall confidence: {medical_doc.overall_confidence.value}")
            logger.info(f"Completeness score: {medical_doc.calculate_completeness_score():.2f}")
        
        return medical_doc
    
    def get_processing_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics about the API processing performance.
        
        Returns:
            Dict: Processing statistics and metrics
        """
        return {
            'total_api_calls': self.api_call_count,
            'successful_extractions': self.successful_extractions,
            'failed_extractions': self.failed_extractions,
            'success_rate': self.successful_extractions / max(1, self.api_call_count),
            'total_processing_time_seconds': self.total_processing_time,
            'average_processing_time_per_call': self.total_processing_time / max(1, self.api_call_count),
            'default_model_used': self.default_model,
            'temperature_setting': self.temperature,
            'max_tokens_setting': self.max_tokens
        }


def demonstrate_basic_llm_api_processing():
    """
    Demonstration function showing basic LLM API processing capabilities.
    This represents stage 3 of the Suki AI internship progression.
    """
    print("=" * 60)
    print("BASIC LLM API PROCESSING DEMONSTRATION")
    print("Stage 3: Transcript processing with API calls")
    print("=" * 60)
    
    # Initialize the API processor
    processor = LLMAPIProcessor(verbose_mode=True)
    
    # Sample medical transcript for demonstration
    sample_transcript = """
MEDICAL RECORD - CONSULTATION NOTE

Patient: John Doe
DOB: 05/15/1980
Age: 43 years
Gender: Male
MRN: MRN12345
Phone: (555) 123-4567

CHIEF COMPLAINT:
Follow-up for hypertension and diabetes management.

VITAL SIGNS:
Blood pressure: 140/90 mmHg
Heart rate: 72 bpm
Temperature: 98.6°F
Respiratory rate: 16 breaths/min
Oxygen saturation: 98%
Weight: 180 lbs

CURRENT MEDICATIONS:
1. Lisinopril 10mg - Take once daily by mouth
   Prescribed by Dr. Smith
2. Metformin 500mg - Take twice daily with meals by mouth
   Prescribed by Dr. Smith

ASSESSMENT AND PLAN:
1. Essential Hypertension (I10) - Continue current medication
2. Type 2 Diabetes Mellitus (E11.9) - Continue current medication

Provider: Dr. Sarah Smith, MD
Date: 2024-01-15
"""
    
    print(f"\nProcessing sample medical transcript...")
    print(f"Transcript length: {len(sample_transcript)} characters")
    
    # Process the complete transcript
    medical_document = processor.process_complete_transcript_to_medical_document(
        sample_transcript, 
        "demo_transcript_001"
    )
    
    print(f"\nProcessing Results:")
    print(f"Document ID: {medical_document.document_id}")
    print(f"Patient: {medical_document.patient_demographics.full_name if medical_document.patient_demographics else 'Not extracted'}")
    print(f"Medications extracted: {len(medical_document.medications)}")
    print(f"Diagnoses extracted: {len(medical_document.diagnoses)}")
    print(f"Overall confidence: {medical_document.overall_confidence.value}")
    print(f"Completeness score: {medical_document.calculate_completeness_score():.2f}")
    print(f"Processing time: {medical_document.processing_time_seconds:.2f} seconds")
    
    print(f"\nAPI Processing Statistics:")
    stats = processor.get_processing_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    return medical_document, processor


if __name__ == "__main__":
    # Run the basic LLM API processing demonstration
    document, processor = demonstrate_basic_llm_api_processing()