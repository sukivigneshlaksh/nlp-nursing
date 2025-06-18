from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field

class Address(BaseModel):
    street: Optional[str] = Field(None, description="Street Address")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State")
    zip_code: Optional[str] = Field(None, description="Zip Code")

class Patient(BaseModel):
    name: Optional[str] = Field(None, description="Patient Name")
    address: Optional[Address] = Field(None, description="Patient Address")
    phone: Optional[str] = Field(None, description="Patient Phone Number")
    dob: Optional[date] = Field(None, description="Patient Date of Birth")
    sex: Optional[str] = Field(None, description="Patient Sex (Male/Female)")
    height: Optional[float] = Field(None, description="Patient Height")
    weight: Optional[float] = Field(None, description="Patient Weight")


class IcdCode(BaseModel):
    code: Optional[str] = Field(None, description="ICD Code")

class Physician(BaseModel):
    npi_or_nsc: Optional[str] = Field(None, description="Physician's NPI or NSC Number")
    phone: Optional[str] = Field(None, description="Physician's Phone Number")

class Supplier(BaseModel):
    phone: Optional[str] = Field(None, description="Supplier's Phone Number")

class PapDeviceForm(BaseModel):
    patient: Patient
    place_of_service: Optional[str] = Field(None, description="Place of Service")
    hicn: Optional[str] = Field(None, description="Health Insurance Claim Number")
    hcpc_code: Optional[str] = Field(None, description="HCPCS Code")
    physician: Physician
    supplier: Supplier
    estimated_length_of_need: Optional[int] = Field(None, description="Estimated Length of Need (in months)")
    icd9_codes: List[IcdCode] = Field(default_factory=list, description="ICD-9 Diagnosis Codes")
    icd10_codes: List[IcdCode] = Field(default_factory=list, description="ICD-10 Diagnosis Codes")
    questions_1_10: List[bool] = Field(default_factory=list, description="Answers to Questions 1-10")
    initial_sleep_test_date: Optional[date] = Field(None, description="Date of Initial Sleep Test")
    first_evaluation_date: Optional[date] = Field(None, description="Date of First Face-to-Face Evaluation")
    first_sleep_test_day: Optional[date] = Field(None, description="Date of First Day of Sleep Test")
    documented_evidence: Optional[bool] = Field(None, description="Documented Evidence of Excessive Daytime Sleepiness, Hypertension, and/or Cardiovascular Disease")
    cpap_tried: Optional[bool] = Field(None, description="CPAP Device Tried and Found Ineffective")
    ahi_rdi: Optional[float] = Field(None, description="Apnea-Hypopnea Index (AHI) or Respiratory Disturbance Index (RDI)")
    follow_up_evaluation_date: Optional[date] = Field(None, description="Date of Follow-up Face-to-Face Evaluation")
    pap_usage: Optional[bool] = Field(None, description="Patient Used PAP 4+ Hours per Night on at Least 70% of Nights in a 30-Day Period")
    symptom_improvement: Optional[bool] = Field(None, description="Improvement in Symptoms of Obstructive Sleep Apnea with the use of PAP")
    narrative_description: Optional[str] = Field(None, description="Narrative Description of Equipment and Cost")
    person_answering_section_b: Optional[str] = Field(None, description="Name of Person Answering Section B Questions")
    title: Optional[str] = Field(None, description="Title")
    employer: Optional[str] = Field(None, description="Employer")
    physician_signature: Optional[str] = Field(None, description="Physician's Signature")
    date_signed: Optional[date] = Field(None, description="Date Signed")