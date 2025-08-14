"""
Medical Data Structures Module
Defines internal representations for medical document processing.
Part of Suki AI internship demonstration - structured data extraction targets.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Union
from datetime import datetime, date
from enum import Enum
import json
import logging

logger = logging.getLogger(__name__)


class DocumentType(Enum):
    """Enumeration of medical document types that can be processed."""
    CLINICAL_NOTE = "clinical_note"
    DISCHARGE_SUMMARY = "discharge_summary"
    LAB_REPORT = "lab_report"
    RADIOLOGY_REPORT = "radiology_report"
    PRESCRIPTION = "prescription"
    INSURANCE_FORM = "insurance_form"
    PROGRESS_NOTE = "progress_note"
    CONSULTATION_NOTE = "consultation_note"
    UNKNOWN = "unknown"


class ExtractionConfidence(Enum):
    """Confidence levels for extracted information."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNCERTAIN = "uncertain"


@dataclass
class PatientDemographics:
    """
    Comprehensive patient demographic information structure.
    Represents core patient identification and demographic data.
    """
    patient_id: Optional[str] = None
    medical_record_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    race: Optional[str] = None
    ethnicity: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_id: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    extraction_confidence: ExtractionConfidence = ExtractionConfidence.UNCERTAIN
    extracted_fields: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert demographics to dictionary format for API processing."""
        return {
            'patient_id': self.patient_id,
            'medical_record_number': self.medical_record_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'age': self.age,
            'gender': self.gender,
            'race': self.race,
            'ethnicity': self.ethnicity,
            'phone_number': self.phone_number,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'insurance_provider': self.insurance_provider,
            'insurance_id': self.insurance_id,
            'emergency_contact_name': self.emergency_contact_name,
            'emergency_contact_phone': self.emergency_contact_phone,
            'extraction_confidence': self.extraction_confidence.value,
            'extracted_fields': self.extracted_fields
        }


@dataclass
class Medication:
    """
    Detailed medication information structure.
    Represents prescription and medication data from medical documents.
    """
    medication_name: Optional[str] = None
    generic_name: Optional[str] = None
    brand_name: Optional[str] = None
    dosage: Optional[str] = None
    dosage_amount: Optional[str] = None
    dosage_unit: Optional[str] = None
    frequency: Optional[str] = None
    route_of_administration: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    prescribing_physician: Optional[str] = None
    pharmacy: Optional[str] = None
    refills_remaining: Optional[int] = None
    ndc_code: Optional[str] = None
    indication: Optional[str] = None
    instructions: Optional[str] = None
    side_effects: List[str] = field(default_factory=list)
    contraindications: List[str] = field(default_factory=list)
    extraction_confidence: ExtractionConfidence = ExtractionConfidence.UNCERTAIN
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert medication to dictionary format for API processing."""
        return {
            'medication_name': self.medication_name,
            'generic_name': self.generic_name,
            'brand_name': self.brand_name,
            'dosage': self.dosage,
            'dosage_amount': self.dosage_amount,
            'dosage_unit': self.dosage_unit,
            'frequency': self.frequency,
            'route_of_administration': self.route_of_administration,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'prescribing_physician': self.prescribing_physician,
            'pharmacy': self.pharmacy,
            'refills_remaining': self.refills_remaining,
            'ndc_code': self.ndc_code,
            'indication': self.indication,
            'instructions': self.instructions,
            'side_effects': self.side_effects,
            'contraindications': self.contraindications,
            'extraction_confidence': self.extraction_confidence.value
        }


@dataclass
class Diagnosis:
    """
    Medical diagnosis information structure.
    Represents diagnostic information extracted from medical documents.
    """
    primary_diagnosis: Optional[str] = None
    secondary_diagnoses: List[str] = field(default_factory=list)
    icd_10_code: Optional[str] = None
    icd_10_description: Optional[str] = None
    diagnosis_date: Optional[date] = None
    diagnosing_physician: Optional[str] = None
    diagnosis_type: Optional[str] = None  # primary, secondary, differential, rule_out
    severity: Optional[str] = None
    status: Optional[str] = None  # active, resolved, chronic, acute
    onset_date: Optional[date] = None
    symptoms: List[str] = field(default_factory=list)
    diagnostic_tests: List[str] = field(default_factory=list)
    treatment_plan: Optional[str] = None
    prognosis: Optional[str] = None
    extraction_confidence: ExtractionConfidence = ExtractionConfidence.UNCERTAIN
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert diagnosis to dictionary format for API processing."""
        return {
            'primary_diagnosis': self.primary_diagnosis,
            'secondary_diagnoses': self.secondary_diagnoses,
            'icd_10_code': self.icd_10_code,
            'icd_10_description': self.icd_10_description,
            'diagnosis_date': self.diagnosis_date.isoformat() if self.diagnosis_date else None,
            'diagnosing_physician': self.diagnosing_physician,
            'diagnosis_type': self.diagnosis_type,
            'severity': self.severity,
            'status': self.status,
            'onset_date': self.onset_date.isoformat() if self.onset_date else None,
            'symptoms': self.symptoms,
            'diagnostic_tests': self.diagnostic_tests,
            'treatment_plan': self.treatment_plan,
            'prognosis': self.prognosis,
            'extraction_confidence': self.extraction_confidence.value
        }


@dataclass
class VitalSigns:
    """
    Patient vital signs information structure.
    Represents physiological measurements from medical documents.
    """
    measurement_datetime: Optional[datetime] = None
    blood_pressure_systolic: Optional[int] = None
    blood_pressure_diastolic: Optional[int] = None
    heart_rate: Optional[int] = None
    respiratory_rate: Optional[int] = None
    temperature: Optional[float] = None
    temperature_unit: Optional[str] = None  # fahrenheit, celsius
    oxygen_saturation: Optional[float] = None
    height: Optional[float] = None
    height_unit: Optional[str] = None  # inches, cm, feet
    weight: Optional[float] = None
    weight_unit: Optional[str] = None  # lbs, kg
    bmi: Optional[float] = None
    pain_scale: Optional[int] = None  # 1-10 scale
    measuring_staff: Optional[str] = None
    measurement_location: Optional[str] = None
    extraction_confidence: ExtractionConfidence = ExtractionConfidence.UNCERTAIN
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert vital signs to dictionary format for API processing."""
        return {
            'measurement_datetime': self.measurement_datetime.isoformat() if self.measurement_datetime else None,
            'blood_pressure_systolic': self.blood_pressure_systolic,
            'blood_pressure_diastolic': self.blood_pressure_diastolic,
            'heart_rate': self.heart_rate,
            'respiratory_rate': self.respiratory_rate,
            'temperature': self.temperature,
            'temperature_unit': self.temperature_unit,
            'oxygen_saturation': self.oxygen_saturation,
            'height': self.height,
            'height_unit': self.height_unit,
            'weight': self.weight,
            'weight_unit': self.weight_unit,
            'bmi': self.bmi,
            'pain_scale': self.pain_scale,
            'measuring_staff': self.measuring_staff,
            'measurement_location': self.measurement_location,
            'extraction_confidence': self.extraction_confidence.value
        }


@dataclass
class Procedure:
    """
    Medical procedure information structure.
    Represents surgical and medical procedures from documents.
    """
    procedure_name: Optional[str] = None
    procedure_code: Optional[str] = None  # CPT code
    procedure_description: Optional[str] = None
    procedure_date: Optional[date] = None
    procedure_time: Optional[str] = None
    performing_physician: Optional[str] = None
    assisting_physicians: List[str] = field(default_factory=list)
    procedure_location: Optional[str] = None
    anesthesia_type: Optional[str] = None
    complications: List[str] = field(default_factory=list)
    outcome: Optional[str] = None
    post_procedure_instructions: Optional[str] = None
    follow_up_required: Optional[bool] = None
    follow_up_date: Optional[date] = None
    procedure_notes: Optional[str] = None
    extraction_confidence: ExtractionConfidence = ExtractionConfidence.UNCERTAIN
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert procedure to dictionary format for API processing."""
        return {
            'procedure_name': self.procedure_name,
            'procedure_code': self.procedure_code,
            'procedure_description': self.procedure_description,
            'procedure_date': self.procedure_date.isoformat() if self.procedure_date else None,
            'procedure_time': self.procedure_time,
            'performing_physician': self.performing_physician,
            'assisting_physicians': self.assisting_physicians,
            'procedure_location': self.procedure_location,
            'anesthesia_type': self.anesthesia_type,
            'complications': self.complications,
            'outcome': self.outcome,
            'post_procedure_instructions': self.post_procedure_instructions,
            'follow_up_required': self.follow_up_required,
            'follow_up_date': self.follow_up_date.isoformat() if self.follow_up_date else None,
            'procedure_notes': self.procedure_notes,
            'extraction_confidence': self.extraction_confidence.value
        }


@dataclass
class LabResult:
    """
    Laboratory test result information structure.
    Represents lab values and test results from medical documents.
    """
    test_name: Optional[str] = None
    test_code: Optional[str] = None
    test_category: Optional[str] = None
    result_value: Optional[str] = None
    result_numeric_value: Optional[float] = None
    reference_range: Optional[str] = None
    unit: Optional[str] = None
    abnormal_flag: Optional[str] = None  # high, low, critical, normal
    test_date: Optional[date] = None
    collection_date: Optional[date] = None
    ordering_physician: Optional[str] = None
    performing_lab: Optional[str] = None
    specimen_type: Optional[str] = None
    test_status: Optional[str] = None  # final, preliminary, corrected
    comments: Optional[str] = None
    critical_value: Optional[bool] = None
    extraction_confidence: ExtractionConfidence = ExtractionConfidence.UNCERTAIN
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert lab result to dictionary format for API processing."""
        return {
            'test_name': self.test_name,
            'test_code': self.test_code,
            'test_category': self.test_category,
            'result_value': self.result_value,
            'result_numeric_value': self.result_numeric_value,
            'reference_range': self.reference_range,
            'unit': self.unit,
            'abnormal_flag': self.abnormal_flag,
            'test_date': self.test_date.isoformat() if self.test_date else None,
            'collection_date': self.collection_date.isoformat() if self.collection_date else None,
            'ordering_physician': self.ordering_physician,
            'performing_lab': self.performing_lab,
            'specimen_type': self.specimen_type,
            'test_status': self.test_status,
            'comments': self.comments,
            'critical_value': self.critical_value,
            'extraction_confidence': self.extraction_confidence.value
        }


@dataclass
class MedicalDocument:
    """
    Comprehensive medical document structure that aggregates all extracted information.
    This is the main internal representation that gets populated by API calls.
    """
    document_id: Optional[str] = None
    document_type: DocumentType = DocumentType.UNKNOWN
    document_date: Optional[date] = None
    facility_name: Optional[str] = None
    department: Optional[str] = None
    attending_physician: Optional[str] = None
    document_title: Optional[str] = None
    raw_text: Optional[str] = None
    
    # Core medical information
    patient_demographics: Optional[PatientDemographics] = None
    medications: List[Medication] = field(default_factory=list)
    diagnoses: List[Diagnosis] = field(default_factory=list)
    vital_signs: List[VitalSigns] = field(default_factory=list)
    procedures: List[Procedure] = field(default_factory=list)
    lab_results: List[LabResult] = field(default_factory=list)
    
    # Document processing metadata
    processing_timestamp: Optional[datetime] = None
    extraction_method: Optional[str] = None
    processing_time_seconds: Optional[float] = None
    api_calls_made: List[str] = field(default_factory=list)
    extraction_errors: List[str] = field(default_factory=list)
    overall_confidence: ExtractionConfidence = ExtractionConfidence.UNCERTAIN
    
    # Additional unstructured information
    clinical_notes: Optional[str] = None
    physician_assessment: Optional[str] = None
    treatment_plan: Optional[str] = None
    discharge_instructions: Optional[str] = None
    follow_up_appointments: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the entire medical document to dictionary format for API processing.
        This is used when sending data to LLM APIs for further processing.
        """
        return {
            'document_id': self.document_id,
            'document_type': self.document_type.value,
            'document_date': self.document_date.isoformat() if self.document_date else None,
            'facility_name': self.facility_name,
            'department': self.department,
            'attending_physician': self.attending_physician,
            'document_title': self.document_title,
            'raw_text': self.raw_text,
            'patient_demographics': self.patient_demographics.to_dict() if self.patient_demographics else None,
            'medications': [med.to_dict() for med in self.medications],
            'diagnoses': [diag.to_dict() for diag in self.diagnoses],
            'vital_signs': [vitals.to_dict() for vitals in self.vital_signs],
            'procedures': [proc.to_dict() for proc in self.procedures],
            'lab_results': [lab.to_dict() for lab in self.lab_results],
            'processing_timestamp': self.processing_timestamp.isoformat() if self.processing_timestamp else None,
            'extraction_method': self.extraction_method,
            'processing_time_seconds': self.processing_time_seconds,
            'api_calls_made': self.api_calls_made,
            'extraction_errors': self.extraction_errors,
            'overall_confidence': self.overall_confidence.value,
            'clinical_notes': self.clinical_notes,
            'physician_assessment': self.physician_assessment,
            'treatment_plan': self.treatment_plan,
            'discharge_instructions': self.discharge_instructions,
            'follow_up_appointments': self.follow_up_appointments
        }
    
    def to_json(self, indent: int = 2) -> str:
        """
        Convert the medical document to JSON string format.
        Useful for saving processed documents or API communication.
        """
        return json.dumps(self.to_dict(), indent=indent, default=str)
    
    def add_processing_note(self, note: str, timestamp: Optional[datetime] = None):
        """
        Add a processing note with timestamp for debugging and audit trails.
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        processing_note = f"[{timestamp.isoformat()}] {note}"
        self.api_calls_made.append(processing_note)
        
        if logger.isEnabledFor(logging.INFO):
            logger.info(f"Processing note added: {processing_note}")
    
    def calculate_completeness_score(self) -> float:
        """
        Calculate a completeness score based on how many fields have been populated.
        Returns a value between 0.0 and 1.0 indicating extraction completeness.
        """
        total_possible_fields = 0
        populated_fields = 0
        
        # Count core document fields
        core_fields = [
            self.document_type != DocumentType.UNKNOWN,
            self.document_date is not None,
            self.facility_name is not None,
            self.attending_physician is not None,
            self.raw_text is not None
        ]
        total_possible_fields += len(core_fields)
        populated_fields += sum(core_fields)
        
        # Count patient demographics fields
        if self.patient_demographics:
            demo_dict = self.patient_demographics.to_dict()
            demo_values = [v for k, v in demo_dict.items() if k not in ['extraction_confidence', 'extracted_fields']]
            total_possible_fields += len(demo_values)
            populated_fields += sum(1 for v in demo_values if v is not None and v != [])
        else:
            total_possible_fields += 15  # approximate number of demo fields
        
        # Count extracted medical data
        medical_data_categories = [
            len(self.medications) > 0,
            len(self.diagnoses) > 0,
            len(self.vital_signs) > 0,
            len(self.procedures) > 0,
            len(self.lab_results) > 0
        ]
        total_possible_fields += len(medical_data_categories)
        populated_fields += sum(medical_data_categories)
        
        if total_possible_fields == 0:
            return 0.0
        
        completeness_score = populated_fields / total_possible_fields
        return min(1.0, max(0.0, completeness_score))


def create_empty_medical_document(document_id: str = None) -> MedicalDocument:
    """
    Factory function to create an empty medical document structure.
    This serves as the starting point for document processing.
    
    Args:
        document_id (str): Optional document identifier
        
    Returns:
        MedicalDocument: Empty medical document ready for population
    """
    return MedicalDocument(
        document_id=document_id or f"doc_{int(datetime.now().timestamp())}",
        processing_timestamp=datetime.now(),
        extraction_method="api_based_extraction",
        overall_confidence=ExtractionConfidence.UNCERTAIN
    )


def demonstrate_data_structures():
    """
    Demonstration function showing the medical data structures.
    This represents the internal representation targets for LLM API extraction.
    """
    print("=" * 60)
    print("MEDICAL DATA STRUCTURES DEMONSTRATION")
    print("Stage 2: Internal representation definition")
    print("=" * 60)
    
    # Create a sample medical document with populated data
    sample_document = create_empty_medical_document("demo_doc_001")
    
    # Populate sample patient demographics
    sample_document.patient_demographics = PatientDemographics(
        patient_id="P12345",
        first_name="John",
        last_name="Doe",
        date_of_birth=date(1980, 5, 15),
        age=43,
        gender="Male",
        extraction_confidence=ExtractionConfidence.HIGH
    )
    
    # Add sample medication
    sample_medication = Medication(
        medication_name="Lisinopril",
        dosage="10mg",
        frequency="Once daily",
        prescribing_physician="Dr. Smith",
        extraction_confidence=ExtractionConfidence.MEDIUM
    )
    sample_document.medications.append(sample_medication)
    
    # Add sample diagnosis
    sample_diagnosis = Diagnosis(
        primary_diagnosis="Hypertension",
        icd_10_code="I10",
        diagnosing_physician="Dr. Smith",
        extraction_confidence=ExtractionConfidence.HIGH
    )
    sample_document.diagnoses.append(sample_diagnosis)
    
    print(f"Sample Medical Document Structure:")
    print(f"Document ID: {sample_document.document_id}")
    print(f"Patient: {sample_document.patient_demographics.first_name} {sample_document.patient_demographics.last_name}")
    print(f"Medications: {len(sample_document.medications)}")
    print(f"Diagnoses: {len(sample_document.diagnoses)}")
    print(f"Completeness Score: {sample_document.calculate_completeness_score():.2f}")
    
    print(f"\nJSON Representation Preview:")
    json_output = sample_document.to_json()
    print(json_output[:500] + "..." if len(json_output) > 500 else json_output)
    
    return sample_document


if __name__ == "__main__":
    # Run the data structures demonstration
    sample_doc = demonstrate_data_structures()