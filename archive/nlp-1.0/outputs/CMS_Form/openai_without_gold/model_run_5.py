from typing import Optional, List
from datetime import date
from pydantic import BaseModel, Field

class TelephoneNumber(BaseModel):
    number: Optional[str] = Field(None, description="Telephone number")

class CertificationType(BaseModel):
    initial_date: Optional[date] = Field(None, description="Initial certification date")
    recertification_date: Optional[date] = Field(None, description="Recertification date")

class PatientInformation(BaseModel):
    name_address: Optional[str] = Field(None, description="Patient name, address, telephone and HICN")
    telephone: Optional[TelephoneNumber] = Field(None, description="Patient telephone number")
    hicn: Optional[str] = Field(None, description="Health Insurance Claim Number")

class SupplierInformation(BaseModel):
    name_address: Optional[str] = Field(None, description="Supplier name, address, telephone and NSC or NPI #")
    telephone: Optional[TelephoneNumber] = Field(None, description="Supplier telephone number")
    nsc_or_npi: Optional[int] = Field(None, description="Supplier NSC or NPI number")

class AdditionalDetails(BaseModel):
    place_of_service: Optional[str] = Field(None, description="Place of service")
    hcpcs_code: Optional[str] = Field(None, description="HCPCS code")
    dob: Optional[date] = Field(None, description="Patient date of birth")
    sex: Optional[str] = Field(None, description="Patient sex (M/F)")
    height: Optional[int] = Field(None, description="Height in inches")
    weight: Optional[int] = Field(None, description="Weight in pounds")

class FacilityInformation(BaseModel):
    facility_name_address: Optional[str] = Field(None, description="Name and address of facility if applicable")
    physician_name_address: Optional[str] = Field(None, description="Physician name and address")

class PhysicianInformation(BaseModel):
    nsc_or_npi: Optional[int] = Field(None, description="Physician's NSC or NPI number")
    telephone: Optional[TelephoneNumber] = Field(None, description="Physician's telephone number")

class InformationAnswers(BaseModel):
    length_of_need: Optional[int] = Field(None, description="Estimated length of need in months")
    diagnosis_codes: Optional[str] = Field(None, description="Diagnosis codes (ICD-9)")

class YesNoQuestion(BaseModel):
    answer: Optional[str] = Field(None, description="Answer to Yes/No question")

class NameOfPersonIfNotPhysician(BaseModel):
    name: Optional[str] = Field(None, description="Name of person if not physician")
    title: Optional[str] = Field(None, description="Title of person")
    employer: Optional[str] = Field(None, description="Employer of person")

class PhysicianAttestation(BaseModel):
    signature: Optional[str] = Field(None, description="Physician's signature")
    date: Optional[date] = Field(None, description="Date of signature")

class CertificateOfMedicalNecessityForm(BaseModel):
    certification_type: CertificationType = Field(default_factory=CertificationType, description="Certification type and date")
    patient_info: PatientInformation = Field(default_factory=PatientInformation, description="Patient information")
    supplier_info: SupplierInformation = Field(default_factory=SupplierInformation, description="Supplier information")
    additional_details: AdditionalDetails = Field(default_factory=AdditionalDetails, description="Additional details")
    facility_info: FacilityInformation = Field(default_factory=FacilityInformation, description="Facility information")
    physician_info: PhysicianInformation = Field(default_factory=PhysicianInformation, description="Physician information")
    information_answers: InformationAnswers = Field(default_factory=InformationAnswers, description="Information answers")
    yes_no_questions: List[YesNoQuestion] = Field(default_factory=list, description="List of Yes/No questions")
    name_of_person: Optional[NameOfPersonIfNotPhysician] = Field(None, description="Name of person if not physician")
    physician_attestation: PhysicianAttestation = Field(default_factory=PhysicianAttestation, description="Physician attestation and signature/date")