from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class Certification(BaseModel):
    date: Optional[date] = Field(None, description="Date of certification")

class PatientInfo(BaseModel):
    name: Optional[str] = Field(None, description="Patient name, address, telephone, and HICN")
    telephone: Optional[str] = Field(None, description="Patient telephone number")
    hicn: Optional[str] = Field(None, description="Health Insurance Claim Number")

class SupplierInfo(BaseModel):
    name: Optional[str] = Field(None, description="Supplier name, address, telephone, and NSC or NPI")
    telephone: Optional[str] = Field(None, description="Supplier telephone number")
    nsc_npi: Optional[int] = Field(None, description="Supplier's NSC or NPI number")

class AdditionalDetails(BaseModel):
    place_of_service: Optional[str] = Field(None, description="Place of service")
    hcpcs_code: Optional[str] = Field(None, description="HCPCS code")
    date_of_birth: Optional[date] = Field(None, description="Patient date of birth")
    sex: Optional[str] = Field(None, description="Sex of the patient (M/F)")
    height: Optional[int] = Field(None, description="Height in inches")
    weight: Optional[int] = Field(None, description="Weight in pounds")

class FacilityInfo(BaseModel):
    name: Optional[str] = Field(None, description="Name and address of facility if applicable")
    physician_name: Optional[str] = Field(None, description="Physician name and address")

class PhysicianInfo(BaseModel):
    nsc_npi: Optional[int] = Field(None, description="Physician's NSC or NPI number")
    telephone: Optional[str] = Field(None, description="Physician's telephone number")

class Information(BaseModel):
    length_of_need: Optional[int] = Field(None, description="Estimated length of need in months")
    diagnosis_codes: Optional[str] = Field(None, description="Diagnosis codes (ICD-9)")

class SectionBQuestions(BaseModel):
    est_length_of_need: Optional[int] = Field(None, description="Estimated length of need (# of months)")
    diagnosis_codes: Optional[str] = Field(None, description="Diagnosis codes (ICD-9)")
    question_1: Optional[str] = Field(None, description="Question 1 response (Y/N/D)")
    question_2_date: Optional[date] = Field(None, description="Question 2 date response")
    question_3_date: Optional[date] = Field(None, description="Question 3 date response")
    question_4: Optional[str] = Field(None, description="Question 4 response (Y/N/D)")
    question_5: Optional[int] = Field(None, description="Answer to question 5")
    question_6: Optional[str] = Field(None, description="Question 6 response (Y/N/D)")
    question_7: Optional[str] = Field(None, description="Question 7 response (Y/N/D)")
    question_8_date: Optional[date] = Field(None, description="Question 8 date response")
    question_9: Optional[str] = Field(None, description="Question 9 response (Y/N)")
    question_10: Optional[str] = Field(None, description="Question 10 response (Y/N)")

class PersonInfo(BaseModel):
    name: Optional[str] = Field(None, description="Name of the person if not physician")
    title: Optional[str] = Field(None, description="Title of the person if not physician")
    employer: Optional[str] = Field(None, description="Employer of the person if not physician")

class PhysicianAttestation(BaseModel):
    signature: Optional[str] = Field(None, description="Physician's signature")
    date: Optional[date] = Field(None, description="Date of physician's signature")

class CertificateOfMedicalNecessity(BaseModel):
    certification: Certification
    patient_info: PatientInfo
    supplier_info: SupplierInfo
    additional_details: AdditionalDetails
    facility_info: FacilityInfo
    physician_info: PhysicianInfo
    information: Information
    section_b_questions: SectionBQuestions
    person_info: PersonInfo
    physician_attestation: PhysicianAttestation