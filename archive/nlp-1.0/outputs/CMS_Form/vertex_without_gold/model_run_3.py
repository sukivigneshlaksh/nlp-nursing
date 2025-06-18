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
    telephone: Optional[str] = Field(None, description="Patient Telephone")
    dob: Optional[date] = Field(None, description="Patient Date of Birth")
    sex: Optional[str] = Field(None, description="Patient Sex (Male/Female)")
    height: Optional[float] = Field(None, description="Patient Height (inches/cm)")
    weight: Optional[float] = Field(None, description="Patient Weight (lbs/kg)")


class IcdCode(BaseModel):
    code: Optional[str] = Field(None, description="ICD Code")

class Physician(BaseModel):
    npi_or_nsc: Optional[str] = Field(None, description="Physician's NPI or NSC Number")
    telephone: Optional[str] = Field(None, description="Physician's Telephone Number")

class Supplier(BaseModel):
    telephone: Optional[str] = Field(None, description="Supplier's Telephone Number")

class SectionB(BaseModel):
    est_length_of_need: Optional[int] = Field(None, description="Estimated Length of Need (in months)")
    icd_9_codes: List[IcdCode] = Field(default_factory=list, description="ICD-9 Diagnosis Codes")
    icd_10_codes: List[IcdCode] = Field(default_factory=list, description="ICD-10 Diagnosis Codes")
    q1_to_q10: List[bool] = Field(default_factory=list, description="Answers to Questions 1-10")
    initial_sleep_test_date: Optional[date] = Field(None, description="Date of Initial Sleep Test")
    first_face_to_face_eval_date: Optional[date] = Field(None, description="Date of First Face-to-Face Evaluation")
    first_day_of_sleep_test: Optional[date] = Field(None, description="Date of First Day of Sleep Test")
    documented_evidence: Optional[bool] = Field(None, description="Documented Evidence of Excessive Daytime Sleepiness, Hypertension, and/or Cardiovascular Disease")
    cpap_tried_and_ineffective: Optional[bool] = Field(None, description="CPAP Device Tried and Found Ineffective?")
    ahi_rdi: Optional[float] = Field(None, description="Apnea-Hypopnea Index (AHI) or Respiratory Disturbance Index (RDI)")
    follow_up_eval_date: Optional[date] = Field(None, description="Date of Follow-up Face-to-Face Evaluation")
    pap_usage: Optional[bool] = Field(None, description="Patient Used PAP 4+ Hours Per Night on at Least 70% of Nights in a 30-Day Period")
    symptoms_improvement: Optional[bool] = Field(None, description="Improvement in Symptoms of Obstructive Sleep Apnea with PAP Use")

class SectionC(BaseModel):
    person_answering_questions: Optional[str] = Field(None, description="Name of Person Answering Section B Questions")
    title: Optional[str] = Field(None, description="Title")
    employer: Optional[str] = Field(None, description="Employer")
    narrative_description: Optional[str] = Field(None, description="Narrative Description of Equipment and Cost")

class CMS10269Form(BaseModel):
    patient: Patient
    place_of_service: Optional[str] = Field(None, description="Place of Service")
    hicn: Optional[str] = Field(None, description="Health Insurance Claim Number")
    hcpc_code: Optional[str] = Field(None, description="HCPCS Code")
    physician: Physician
    supplier: Supplier
    section_b: SectionB
    section_c: SectionC
    physician_signature: Optional[str] = Field(None, description="Physician's Signature")
    date: Optional[date] = Field(None, description="Date")