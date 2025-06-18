from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class ContactInfo(BaseModel):
    name: Optional[str] = Field(None, description="Full name")
    telephone: Optional[str] = Field(None, description="Telephone number")
    address: Optional[str] = Field(None, description="Address")

class CertificationType(BaseModel):
    initial_date: Optional[date] = Field(None, description="Initial certification date")
    recertification_date: Optional[date] = Field(None, description="Recertification date")

class PatientInfo(ContactInfo):
    hicn: Optional[str] = Field(None, description="HICN")

class SupplierInfo(ContactInfo):
    nsc_or_npi: Optional[int] = Field(None, description="NSC or NPI number")

class FacilityInfo(ContactInfo):
    pass

class PhysicianInfo(ContactInfo):
    nsc_or_npi: Optional[int] = Field(None, description="Physician's NSC or NPI number")

class AdditionalDetails(BaseModel):
    place_of_service: Optional[str] = Field(None, description="Place of service")
    hcpcs_code: Optional[str] = Field(None, description="HCPCS code")
    patient_dob: Optional[date] = Field(None, description="Patient date of birth")
    sex: Optional[str] = Field(None, description="Sex (Male/Female)")
    height: Optional[int] = Field(None, description="Height in inches")
    weight: Optional[int] = Field(None, description="Weight in pounds")

class SectionBInfo(BaseModel):
    length_of_need: Optional[int] = Field(None, description="Estimated length of need in months")
    diagnosis_codes: Optional[str] = Field(None, description="Diagnosis codes (ICD-9)")
    question_1: Optional[str] = Field(None, description="Question 1 response (Y/N/D)")
    question_2_date: Optional[date] = Field(None, description="Question 2 date")
    question_3_date: Optional[date] = Field(None, description="Question 3 date")
    question_4: Optional[str] = Field(None, description="Question 4 response (Y/N/D)")
    question_5: Optional[int] = Field(None, description="Question 5 number")
    question_6: Optional[str] = Field(None, description="Question 6 response (Y/N/D)")
    question_7: Optional[str] = Field(None, description="Question 7 response (Y/N/D)")
    question_8_date: Optional[date] = Field(None, description="Question 8 date")
    question_9: Optional[str] = Field(None, description="Question 9 response (Y/N)")
    question_10: Optional[str] = Field(None, description="Question 10 response (Y/N)")

class RepresentativeInfo(BaseModel):
    name: Optional[str] = Field(None, description="Name of person, if not physician")
    title: Optional[str] = Field(None, description="Title of person, if not physician")
    employer: Optional[str] = Field(None, description="Employer of person, if not physician")

class PhysicianAttestation(BaseModel):
    signature: Optional[str] = Field(None, description="Physician's signature")
    date: Optional[date] = Field(None, description="Date of attestation")

class CertificateOfMedicalNecessity(BaseModel):
    certification_type: CertificationType = Field(description="Certification type and dates")
    patient_info: PatientInfo = Field(description="Patient's information")
    supplier_info: SupplierInfo = Field(description="Supplier's information")
    additional_details: AdditionalDetails = Field(description="Additional details")
    facility_info: Optional[FacilityInfo] = Field(None, description="Facility information, if applicable")
    physician_info: PhysicianInfo = Field(description="Physician's information")
    section_b_info: SectionBInfo = Field(description="Section B information and answers")
    representative_info: Optional[RepresentativeInfo] = Field(None, description="Representative information, if not physician")
    physician_attestation: PhysicianAttestation = Field(description="Physician attestation and signature")