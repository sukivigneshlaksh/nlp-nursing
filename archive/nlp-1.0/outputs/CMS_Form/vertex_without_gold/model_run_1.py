from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field

class Address(BaseModel):
    street: Optional[str] = Field(None, description="Street address")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State")
    zip_code: Optional[str] = Field(None, description="Zip code")

class Patient(BaseModel):
    name: Optional[str] = Field(None, description="Patient's full name")
    address: Optional[Address] = Field(None, description="Patient's address")
    telephone: Optional[str] = Field(None, description="Patient's telephone number")
    dob: Optional[date] = Field(None, description="Patient's date of birth")
    sex: Optional[str] = Field(None, description="Patient's sex (Male/Female)")
    height: Optional[float] = Field(None, description="Patient's height")
    weight: Optional[float] = Field(None, description="Patient's weight")
    hicn: Optional[str] = Field(None, description="Health Insurance Claim Number")

class Physician(BaseModel):
    npi_or_nsc: Optional[str] = Field(None, description="Physician's NPI or NSC number")
    telephone: Optional[str] = Field(None, description="Physician's telephone number")

class Supplier(BaseModel):
    telephone: Optional[str] = Field(None, description="Supplier's telephone number")

class DiagnosisCode(BaseModel):
    code: Optional[str] = Field(None, description="ICD-9 or ICD-10 code")

class Question(BaseModel):
    question_number: int
    answer: bool

class PapForm(BaseModel):
    patient: Patient
    place_of_service: Optional[str] = Field(None, description="Place of service")
    hcpc_code: Optional[str] = Field(None, description="HCPCS code")
    physician: Physician
    supplier: Supplier
    estimated_length_of_need: Optional[int] = Field(None, description="Estimated length of need in months")
    icd9_codes: List[DiagnosisCode] = Field(default_factory=list, description="List of ICD-9 diagnosis codes")
    icd10_codes: List[DiagnosisCode] = Field(default_factory=list, description="List of ICD-10 diagnosis codes")
    obstructive_sleep_apnea_questions: List[Question] = Field(default_factory=list, description="Answers to questions about obstructive sleep apnea")
    initial_sleep_test_date: Optional[date] = Field(None, description="Date of initial sleep test")
    first_face_to_face_evaluation_date: Optional[date] = Field(None, description="Date of patient's first face-to-face evaluation")
    sleep_test_first_day: Optional[date] = Field(None, description="Date of first day of sleep test (if spans multiple days)")
    documented_evidence_of_symptoms: bool = Field(..., description="Does the patient have documented evidence of symptoms?")
    cpap_device_tried: Optional[bool] = Field(None, description="Has a CPAP device been tried and found ineffective?")
    ahi_or_rdi: Optional[float] = Field(None, description="Patient's Apnea-Hypopnea Index (AHI) or Respiratory Disturbance Index (RDI)")
    follow_up_evaluation_date: Optional[date] = Field(None, description="Date of follow-up face-to-face evaluation")
    pap_usage_documented: bool = Field(..., description="Is there active documentation that the patient used PAP 4+ hours per night?")
    pap_improved_symptoms: bool = Field(..., description="Did the use of PAP improve symptoms of obstructive sleep apnea?")
    name_answering_section_b: Optional[str] = Field(None, description="Name of person answering Section B questions")
    title: Optional[str] = Field(None, description="Title")
    employer: Optional[str] = Field(None, description="Employer")
    narrative_description: Optional[str] = Field(None, description="Narrative description of equipment and cost")
    physician_signature: Optional[str] = Field(None, description="Physician's signature")
    date_signed: Optional[date] = Field(None, description="Date signed")
    npi: Optional[str] = Field(None, description="National Provider Identifier")