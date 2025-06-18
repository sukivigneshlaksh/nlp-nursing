from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class CertificationTypeDate(BaseModel):
    initial_date: Optional[date] = Field(None, description="Initial certification date")
    recertification_date: Optional[date] = Field(None, description="Recertification date")

class PatientInformation(BaseModel):
    name_address_telephone_hicn: Optional[str] = Field(None, description="Patient name, address, telephone and HICN")
    telephone: Optional[str] = Field(None, description="Patient telephone number")
    hicn: Optional[str] = Field(None, description="Patient HICN")

class SupplierInformation(BaseModel):
    name_address_telephone_nsc_npi: Optional[str] = Field(None, description="Supplier name, address, telephone and NSC or NPI")
    telephone: Optional[str] = Field(None, description="Supplier telephone number")
    nsc_npi: Optional[int] = Field(None, description="Supplier NSC or NPI number")

class AdditionalDetails(BaseModel):
    place_of_service: Optional[str] = Field(None, description="Place of service")
    hcpcs_code: Optional[str] = Field(None, description="HCPCS code")
    pt_dob: Optional[date] = Field(None, description="Patient date of birth")
    sex: Optional[str] = Field(None, description="Patient Sex (M/F)")
    height: Optional[int] = Field(None, description="Patient height in inches")
    weight: Optional[int] = Field(None, description="Patient weight in lbs")

class FacilityInformation(BaseModel):
    facility_name_address: Optional[str] = Field(None, description="Name and address of facility if applicable")
    physician_name_address: Optional[str] = Field(None, description="Physician name and address (Printed or Typed)")

class PhysicianInformation(BaseModel):
    nsc_npi: Optional[int] = Field(None, description="Physician’s NSC or NPI number")
    telephone: Optional[str] = Field(None, description="Physician’s telephone number")

class SectionBInformation(BaseModel):
    length_of_need: Optional[int] = Field(None, description="Estimated length of need in months")
    diagnosis_codes: Optional[str] = Field(None, description="Diagnosis codes (ICD-9)")
    question_1: Optional[str] = Field(None, description="Question 1 answer (Y/N/D)")
    question_2: Optional[date] = Field(None, description="Question 2 date")
    question_3: Optional[date] = Field(None, description="Question 3 date")
    question_4: Optional[str] = Field(None, description="Question 4 answer (Y/N/D)")
    question_5: Optional[int] = Field(None, description="Question 5 number")
    question_6: Optional[str] = Field(None, description="Question 6 answer (Y/N/D)")
    question_7: Optional[str] = Field(None, description="Question 7 answer (Y/N/D)")
    question_8: Optional[date] = Field(None, description="Question 8 date")
    question_9: Optional[str] = Field(None, description="Question 9 answer (Y/N)")
    question_10: Optional[str] = Field(None, description="Question 10 answer (Y/N)")

class NameOfPerson(BaseModel):
    name: Optional[str] = Field(None, description="Name of person (if not Physician)")
    title: Optional[str] = Field(None, description="Title of person")
    employer: Optional[str] = Field(None, description="Employer of person")

class PhysicianAttestation(BaseModel):
    signature: Optional[str] = Field(None, description="Physician’s signature")
    date: Optional[date] = Field(None, description="Date of signature")

class CertificateOfMedicalNecessity(BaseModel):
    certification_type_date: CertificationTypeDate = Field(default_factory=CertificationTypeDate, description="Certification type/date information")
    patient_information: PatientInformation = Field(default_factory=PatientInformation, description="Patient information")
    supplier_information: SupplierInformation = Field(default_factory=SupplierInformation, description="Supplier information")
    additional_details: AdditionalDetails = Field(default_factory=AdditionalDetails, description="Additional details")
    facility_information: FacilityInformation = Field(default_factory=FacilityInformation, description="Facility information")
    physician_information: PhysicianInformation = Field(default_factory=PhysicianInformation, description="Physician information")
    section_b_information: SectionBInformation = Field(default_factory=SectionBInformation, description="Section B: Information (Answers)")
    name_of_person: NameOfPerson = Field(default_factory=NameOfPerson, description="Name of person if not the physician")
    physician_attestation: PhysicianAttestation = Field(default_factory=PhysicianAttestation, description="Physician attestation and signature/date")