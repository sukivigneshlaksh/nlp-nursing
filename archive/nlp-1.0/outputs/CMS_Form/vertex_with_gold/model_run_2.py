from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class Address(BaseModel):
    street: Optional[str] = Field(None, description="Street address")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State")
    zip_code: Optional[str] = Field(None, description="Zip code")

class PatientInfo(BaseModel):
    name: Optional[str] = Field(None, description="Patient's full name")
    address: Optional[Address] = Field(None, description="Patient's address")
    phone: Optional[str] = Field(None, description="Patient's phone number")
    npi: Optional[str] = Field(None, description="National Provider Identifier")
    dob: Optional[date] = Field(None, description="Patient's date of birth")
    sex: Optional[str] = Field(None, description="Patient's sex (Male/Female)")
    height: Optional[float] = Field(None, description="Patient's height")
    weight: Optional[float] = Field(None, description="Patient's weight")


class PhysicianInfo(BaseModel):
    npi_or_nsc: Optional[str] = Field(None, description="Physician's NPI or NSC number")
    phone: Optional[str] = Field(None, description="Physician's phone number")

class SupplierInfo(BaseModel):
    phone: Optional[str] = Field(None, description="Supplier's phone number")


class DiagnosisCode(BaseModel):
    code: Optional[str] = Field(None, description="ICD-9 or ICD-10 code")


class PapForm(BaseModel):
    patient: PatientInfo = Field(..., description="Patient information")
    place_of_service: Optional[str] = Field(None, description="Place of service")
    hicn: Optional[str] = Field(None, description="Health Insurance Claim Number")
    hcpc_code: Optional[str] = Field(None, description="HCPCS code")
    physician: PhysicianInfo = Field(..., description="Physician information")
    supplier: SupplierInfo = Field(..., description="Supplier information")
    estimated_length_of_need: Optional[int] = Field(None, description="Estimated length of need in months")
    icd9_codes: List[DiagnosisCode] = Field(default_factory=list, description="List of ICD-9 diagnosis codes")
    icd10_codes: List[DiagnosisCode] = Field(default_factory=list, description="List of ICD-10 diagnosis codes")
    questions_1_10: List[bool] = Field(default_factory=list, description="Answers to questions 1-10")
    initial_sleep_test_date: Optional[date] = Field(None, description="Date of initial sleep test")
    first_evaluation_date: Optional[date] = Field(None, description="Date of patient's first face-to-face evaluation")
    first_day_of_sleep_test: Optional[date] = Field(None, description="Date of first day of sleep test (if spans multiple days)")
    documented_evidence: Optional[bool] = Field(None, description="Documented evidence of excessive daytime sleepiness, hypertension, and/or cardiovascular disease")
    cpap_tried_and_ineffective: Optional[bool] = Field(None, description="CPAP device tried and found ineffective")
    ahi_or_rdi: Optional[float] = Field(None, description="Patient's Apnea-Hypopnea Index (AHI) or Respiratory Disturbance Index (RDI)")
    follow_up_evaluation_date: Optional[date] = Field(None, description="Date of follow-up face-to-face evaluation")
    pap_usage: Optional[bool] = Field(None, description="Patient used PAP 4+ hours per night on at least 70% of nights in a 30-day period")
    symptom_improvement: Optional[bool] = Field(None, description="Improvement in symptoms of obstructive sleep apnea with the use of PAP")
    narrative_contact_person: Optional[str] = Field(None, description="Name of person answering Section B questions")
    narrative_contact_title: Optional[str] = Field(None, description="Title of narrative contact person")
    narrative_contact_employer: Optional[str] = Field(None, description="Employer of narrative contact person")
    narrative_description: Optional[str] = Field(None, description="Narrative description of equipment and cost")
    physician_signature: Optional[str] = Field(None, description="Physician's signature")
    physician_signature_date: Optional[date] = Field(None, description="Date of physician's signature")