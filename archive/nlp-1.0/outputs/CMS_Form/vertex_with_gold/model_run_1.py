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
    telephone: Optional[str] = Field(None, description="Patient's telephone number")
    npi: Optional[str] = Field(None, description="Patient's NPI number")

class PhysicianInfo(BaseModel):
    npi_or_nsc: Optional[str] = Field(None, description="Physician's NPI or NSC number")
    telephone: Optional[str] = Field(None, description="Physician's telephone number")

class SupplierInfo(BaseModel):
    telephone: Optional[str] = Field(None, description="Supplier's telephone number")

class IcdCode(BaseModel):
    code: Optional[str] = Field(None, description="ICD code")

class PapForm(BaseModel):
    patient: PatientInfo = Field(..., description="Patient information")
    place_of_service: Optional[str] = Field(None, description="Place of service")
    hicn: Optional[str] = Field(None, description="Health Insurance Claim Number")
    hcpc_code: Optional[str] = Field(None, description="HCPCS code")
    dob: Optional[date] = Field(None, description="Patient's date of birth")
    sex: Optional[str] = Field(None, description="Patient's sex (Male/Female)")
    height: Optional[float] = Field(None, description="Patient's height")
    weight: Optional[float] = Field(None, description="Patient's weight")
    physician: PhysicianInfo = Field(..., description="Physician information")
    supplier: SupplierInfo = Field(..., description="Supplier information")
    estimated_length_of_need: Optional[int] = Field(None, description="Estimated length of need in months")
    icd9_codes: List[IcdCode] = Field(default_factory=list, description="List of ICD-9 diagnosis codes")
    icd10_codes: List[IcdCode] = Field(default_factory=list, description="List of ICD-10 diagnosis codes")
    obstructive_sleep_apnea_questions: List[bool] = Field(default_factory=list, description="Answers to questions 1-10 for Obstructive Sleep Apnea")
    initial_sleep_test_date: Optional[date] = Field(None, description="Date of initial sleep test")
    first_face_to_face_evaluation_date: Optional[date] = Field(None, description="Date of patient's first face-to-face evaluation")
    first_day_of_sleep_test_date: Optional[date] = Field(None, description="Date of first day of sleep test (if spans multiple days)")
    documented_evidence_of_symptoms: Optional[bool] = Field(None, description="Does the patient have documented evidence of excessive daytime sleepiness, hypertension, and/or cardiovascular disease?")
    cpap_device_tried: Optional[bool] = Field(None, description="If a bilevel device ordered, has a CPAP device been tried and found ineffective?")
    ahi_or_rdi: Optional[float] = Field(None, description="Patient's Apnea-Hypopnea Index (AHI) or respiratory disturbance index (RDI)")
    follow_up_evaluation_date: Optional[date] = Field(None, description="Date of follow-up face-to-face evaluation")
    pap_usage_documented: Optional[bool] = Field(None, description="Is there active documentation that the patient used PAP 4+ hours per night on at least 70% of nights in a 30-day period?")
    improvement_in_symptoms: Optional[bool] = Field(None, description="Did the report period show improvement in symptoms of obstructive sleep apnea with the use of PAP?")
    narrative_description: Optional[str] = Field(None, description="Narrative description of equipment and cost")
    person_answering_section_b: Optional[str] = Field(None, description="Name of person answering Section B questions")
    title: Optional[str] = Field(None, description="Title")
    employer: Optional[str] = Field(None, description="Employer")
    physician_signature: Optional[str] = Field(None, description="Physician's signature")
    date_signed: Optional[date] = Field(None, description="Date signed")