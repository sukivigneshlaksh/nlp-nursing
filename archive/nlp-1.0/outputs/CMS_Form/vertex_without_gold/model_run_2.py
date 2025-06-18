from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field

class Address(BaseModel):
    street: Optional[str] = Field(None, description="Street address")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State")
    zip_code: Optional[str] = Field(None, description="Zip code")

class PatientInfo(BaseModel):
    name: Optional[str] = Field(None, description="Patient's full name")
    address: Optional[Address] = Field(None, description="Patient's address")
    phone: Optional[str] = Field(None, description="Patient's phone number")
    dob: Optional[date] = Field(None, description="Patient's date of birth")
    sex: Optional[str] = Field(None, description="Patient's sex (Male/Female)")
    height: Optional[float] = Field(None, description="Patient's height")
    weight: Optional[float] = Field(None, description="Patient's weight")
    hicn: Optional[str] = Field(None, description="Health Insurance Claim Number")


class PhysicianInfo(BaseModel):
    npi_or_nsc: Optional[str] = Field(None, description="Physician's NPI or NSC number")
    phone: Optional[str] = Field(None, description="Physician's phone number")

class SupplierInfo(BaseModel):
    phone: Optional[str] = Field(None, description="Supplier's phone number")

class DiagnosisCode(BaseModel):
    code: Optional[str] = Field(None, description="ICD-9 or ICD-10 code")

class SleepApneaQuestion(BaseModel):
    question_number: int
    answer: bool

class PapDeviceForm(BaseModel):
    patient: PatientInfo
    place_of_service: Optional[str] = Field(None, description="Place of service")
    hcpc_code: Optional[str] = Field(None, description="HCPCS code")
    physician: PhysicianInfo
    supplier: SupplierInfo
    estimated_length_of_need: Optional[int] = Field(None, description="Estimated length of need (in months)")
    icd9_diagnosis_codes: List[DiagnosisCode] = Field(default_factory=list, description="List of ICD-9 diagnosis codes")
    icd10_diagnosis_codes: List[DiagnosisCode] = Field(default_factory=list, description="List of ICD-10 diagnosis codes")
    sleep_apnea_questions: List[SleepApneaQuestion] = Field(default_factory=list, description="Answers to sleep apnea questions")
    initial_sleep_test_date: Optional[date] = Field(None, description="Date of initial sleep test")
    first_face_to_face_evaluation_date: Optional[date] = Field(None, description="Date of patient's first face-to-face evaluation")
    first_day_of_sleep_test: Optional[date] = Field(None, description="Date of first day of sleep test (if spans multiple days)")
    documented_evidence_of_symptoms: bool = Field(..., description="Does the patient have documented evidence of excessive daytime sleepiness, hypertension, and/or cardiovascular disease?")
    cpap_tried_and_ineffective: Optional[bool] = Field(None, description="If a bilevel device ordered, has a CPAP device been tried and found ineffective?")
    ahi_rdi: Optional[float] = Field(None, description="Patient's Apnea-Hypopnea Index (AHI) or Respiratory Disturbance Index (RDI)")
    follow_up_evaluation_date: Optional[date] = Field(None, description="Date of follow-up face-to-face evaluation")
    pap_usage_documented: Optional[bool] = Field(None, description="Is there active documentation that the patient used PAP 4+ hours per night on at least 70% of nights in a 30-day period?")
    improvement_in_symptoms: Optional[bool] = Field(None, description="Did the report period show improvement in symptoms of obstructive sleep apnea with the use of PAP?")
    section_b_respondent_name: Optional[str] = Field(None, description="Name of person answering Section B questions")
    section_b_respondent_title: Optional[str] = Field(None, description="Title of person answering Section B questions")
    section_b_respondent_employer: Optional[str] = Field(None, description="Employer of person answering Section B questions")
    equipment_description: Optional[str] = Field(None, description="Narrative description of equipment")
    physician_signature: Optional[str] = Field(None, description="Physician's signature")
    date_signed: Optional[date] = Field(None, description="Date signed")