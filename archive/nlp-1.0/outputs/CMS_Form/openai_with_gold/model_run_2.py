from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class CertificationTypeDate(BaseModel):
    initial_date: Optional[date] = Field(None, description="Date of initial certification")
    recertification_date: Optional[date] = Field(None, description="Date of recertification")

class PatientInformation(BaseModel):
    name: Optional[str] = Field(None, description="Patient name, address, and HICN")
    telephone_number: Optional[str] = Field(None, description="Patient's telephone number")
    hicn: Optional[str] = Field(None, description="Patient's HICN")

class SupplierInformation(BaseModel):
    name: Optional[str] = Field(None, description="Supplier name, address, and telephone")
    telephone_number: Optional[str] = Field(None, description="Supplier's telephone number")
    nsc_or_npi: Optional[int] = Field(None, description="NSC or NPI number of supplier")

class AdditionalDetails(BaseModel):
    place_of_service: Optional[str] = Field(None, description="Place of service")
    hcpcs_code: Optional[str] = Field(None, description="HCPCS code")
    dob: Optional[date] = Field(None, description="Patient date of birth")
    sex: Optional[str] = Field(None, description="Patient sex, Male/Female")
    height: Optional[int] = Field(None, description="Height in inches")
    weight: Optional[int] = Field(None, description="Weight in pounds")

class FacilityInformation(BaseModel):
    name_and_address: Optional[str] = Field(None, description="Facility name and address")
    physician_name_and_address: Optional[str] = Field(None, description="Physician name and address")

class PhysicianInformation(BaseModel):
    nsc_or_npi: Optional[int] = Field(None, description="Physician's NSC or NPI number")
    telephone_number: Optional[str] = Field(None, description="Physician's telephone number")

class SectionBInformation(BaseModel):
    length_of_need: Optional[int] = Field(None, description="Estimated length of need in months")
    diagnosis_codes: Optional[str] = Field(None, description="Diagnosis codes (ICD-9)")
    question_1: Optional[str] = Field(None, description="Answer to question 1: Yes/No/Does Not Apply")
    date_2: Optional[date] = Field(None, description="Date for question 2")
    date_3: Optional[date] = Field(None, description="Date for question 3")
    question_4: Optional[str] = Field(None, description="Answer to question 4: Yes/No/Does Not Apply")
    question_5: Optional[int] = Field(None, description="Numeric answer to question 5")
    question_6: Optional[str] = Field(None, description="Answer to question 6: Yes/No/Does Not Apply")
    question_7: Optional[str] = Field(None, description="Answer to question 7: Yes/No/Does Not Apply")
    date_8: Optional[date] = Field(None, description="Date for question 8")
    question_9: Optional[str] = Field(None, description="Answer to question 9: Yes/No")
    question_10: Optional[str] = Field(None, description="Answer to question 10: Yes/No")

class PersonInformation(BaseModel):
    name: Optional[str] = Field(None, description="Name of the person if not a physician")
    title: Optional[str] = Field(None, description="Title of the person")
    employer: Optional[str] = Field(None, description="Employer of the person")

class PhysicianAttestation(BaseModel):
    signature: Optional[str] = Field(None, description="Physician's signature")
    date: Optional[date] = Field(None, description="Date of physician's signature")

class CertificateOfMedicalNecessity(BaseModel):
    certification_type_date: CertificationTypeDate = Field(..., description="Certification type and date details")
    patient_information: PatientInformation = Field(..., description="Patient information details")
    supplier_information: SupplierInformation = Field(..., description="Supplier information details")
    additional_details: AdditionalDetails = Field(..., description="Additional details")
    facility_information: FacilityInformation = Field(..., description="Facility information details")
    physician_information: PhysicianInformation = Field(..., description="Physician information details")
    section_b_information: SectionBInformation = Field(..., description="Section B information and answers")
    person_information: PersonInformation = Field(..., description="Information of person, if not a physician")
    physician_attestation: PhysicianAttestation = Field(..., description="Physician attestation and signature")