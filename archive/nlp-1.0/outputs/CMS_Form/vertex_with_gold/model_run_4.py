from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class Address(BaseModel):
    street: Optional[str] = Field(None, description="Street address")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State")
    zip_code: Optional[str] = Field(None, description="Zip code")

class PatientInformation(BaseModel):
    name: Optional[str] = Field(None, description="Patient's full name")
    address: Optional[Address] = Field(None, description="Patient's address")
    phone: Optional[str] = Field(None, description="Patient's phone number")
    npi: Optional[str] = Field(None, description="Patient's NPI number")


class IcdCode(BaseModel):
    code: Optional[str] = Field(None, description="ICD code")

class PhysicianInformation(BaseModel):
    npi_or_nsc: Optional[str] = Field(None, description="Physician's NPI or NSC number")
    phone: Optional[str] = Field(None, description="Physician's phone number")

class SupplierInformation(BaseModel):
    phone: Optional[str] = Field(None, description="Supplier's phone number")

class PapForm(BaseModel):
    patient: PatientInformation = Field(..., description="Patient Information")
    place_of_service: Optional[str] = Field(None, description="Place of service")
    hicn: Optional[str] = Field(None, description="Health Insurance Claim Number")
    hcpcs_code: Optional[str] = Field(None, description="HCPCS code")
    dob: Optional[date] = Field(None, description="Patient's date of birth")
    sex: Optional[str] = Field(None, description="Patient's sex (Male/Female)")
    height: Optional[float] = Field(None, description="Patient's height")
    weight: Optional[float] = Field(None, description="Patient's weight")
    physician: PhysicianInformation = Field(..., description="Physician Information")
    supplier: SupplierInformation = Field(..., description="Supplier Information")
    estimated_length_of_need: Optional[int] = Field(None, description="Estimated length of need in months")
    icd9_codes: List[IcdCode] = Field(default_factory=list, description="List of ICD-9 diagnosis codes")
    icd10_codes: List[IcdCode] = Field(default_factory=list, description="List of ICD-10 diagnosis codes")
    questions_1_10: List[bool] = Field(default_factory=list, description="Answers to questions 1-10 (True/False)")
    initial_sleep_test_date: Optional[date] = Field(None, description="Date of initial sleep test")
    first_evaluation_date: Optional[date] = Field(None, description="Date of patient's first face-to-face evaluation")
    first_day_of_test: Optional[date] = Field(None, description="Date of first day of sleep test (if spans multiple days)")
    documented_evidence: List[bool] = Field(default_factory=list, description="Documented evidence of excessive daytime sleepiness, hypertension, and/or cardiovascular disease (True/False)")
    cpap_tried_and_ineffective: Optional[bool] = Field(None, description="Was a CPAP device tried and found ineffective? (True/False)")
    ahi_or_rdi: Optional[float] = Field(None, description="Patient's Apnea-Hypopnea Index (AHI) or Respiratory Disturbance Index (RDI)")
    follow_up_evaluation_date: Optional[date] = Field(None, description="Date of follow-up face-to-face evaluation")
    pap_usage: Optional[bool] = Field(None, description="Did the patient use PAP 4+ hours per night on at least 70% of nights in a 30-day period? (True/False)")
    symptoms_improvement: Optional[bool] = Field(None, description="Did the patient experience improvement in symptoms of obstructive sleep apnea with the use of PAP? (True/False)")
    section_b_respondent_name: Optional[str] = Field(None, description="Name of person answering Section B questions")
    section_b_respondent_title: Optional[str] = Field(None, description="Title of person answering Section B questions")
    section_b_respondent_employer: Optional[str] = Field(None, description="Employer of person answering Section B questions")
    equipment_description: Optional[str] = Field(None, description="Narrative description of equipment")
    physician_signature: Optional[str] = Field(None, description="Physician's signature")
    date_signed: Optional[date] = Field(None, description="Date of signature")