from typing import Optional, List
from datetime import date
from pydantic import BaseModel, Field

class PatientInformation(BaseModel):
    name: Optional[str] = Field(None, description="Patient name, address, telephone, and HICN")
    telephone_number: Optional[str] = Field(None, description="Patient telephone number")
    hicn: Optional[str] = Field(None, description="Patient HICN")

class SupplierInformation(BaseModel):
    name: Optional[str] = Field(None, description="Supplier name, address, telephone, and NSC or NPI #")
    telephone_number: Optional[str] = Field(None, description="Supplier telephone number")
    nsc_or_npi: Optional[int] = Field(None, description="Supplier NSC or NPI number")

class FacilityInformation(BaseModel):
    name_and_address: Optional[str] = Field(None, description="Name and address of facility if applicable")
    physician_name_and_address: Optional[str] = Field(None, description="Physician name and address (printed or typed)")

class PhysicianInformation(BaseModel):
    nsc_or_npi: Optional[int] = Field(None, description="Physician's NSC or NPI number")
    telephone_number: Optional[str] = Field(None, description="Physician's telephone number")

class PersonInformation(BaseModel):
    name: Optional[str] = Field(None, description="Name of the person if not physician")
    title: Optional[str] = Field(None, description="Title of the person if not physician")
    employer: Optional[str] = Field(None, description="Employer of the person if not physician")

class CertificationTypeDate(BaseModel):
    initial_date: Optional[date] = Field(None, description="Initial certification date")
    recertification_date: Optional[date] = Field(None, description="Recertification date")

class AdditionalDetails(BaseModel):
    place_of_service: Optional[str] = Field(None, description="Place of service")
    hcpcs_code: Optional[str] = Field(None, description="HCPCS code")
    pt_dob: Optional[date] = Field(None, description="Patient date of birth")
    sex: Optional[str] = Field(None, description="Patient sex (M/F)")
    height: Optional[int] = Field(None, description="Patient height in inches")
    weight: Optional[int] = Field(None, description="Patient weight in pounds")

class SectionBInformation(BaseModel):
    length_of_need: Optional[int] = Field(None, description="Estimated length of need in months")
    diagnosis_codes: Optional[str] = Field(None, description="Diagnosis codes (ICD-9)")
    question_1: Optional[str] = Field(None, description="Question 1: Yes/No/Does Not Apply")
    question_2: Optional[date] = Field(None, description="Question 2: Date")
    question_3: Optional[date] = Field(None, description="Question 3: Date")
    question_4: Optional[str] = Field(None, description="Question 4: Yes/No/Does Not Apply")
    question_5: Optional[int] = Field(None, description="Question 5: Number")
    question_6: Optional[str] = Field(None, description="Question 6: Yes/No/Does Not Apply")
    question_7: Optional[str] = Field(None, description="Question 7: Yes/No/Does Not Apply")
    question_8: Optional[date] = Field(None, description="Question 8: Date")
    question_9: Optional[str] = Field(None, description="Question 9: Yes/No")
    question_10: Optional[str] = Field(None, description="Question 10: Yes/No")

class PhysicianAttestation(BaseModel):
    signature: Optional[str] = Field(None, description="Physician's signature")
    date: Optional[date] = Field(None, description="Date of physician's signature")

class CertificateOfMedicalNecessityForm(BaseModel):
    certification_type_date: CertificationTypeDate = Field(..., description="Certification type and date")
    patient_information: PatientInformation = Field(..., description="Patient information")
    supplier_information: SupplierInformation = Field(..., description="Supplier information")
    additional_details: AdditionalDetails = Field(..., description="Additional details")
    facility_information: FacilityInformation = Field(..., description="Facility information")
    physician_information: PhysicianInformation = Field(..., description="Physician information")
    section_b_information: SectionBInformation = Field(..., description="Section B information")
    person_information: PersonInformation = Field(..., description="Name of person if not physician")
    physician_attestation: PhysicianAttestation = Field(..., description="Physician attestation and signature date")