from typing import Optional, List
from datetime import date
from pydantic import BaseModel, Field

class CertificationTypeDate(BaseModel):
    initial: Optional[date] = Field(None, description="Initial certification date")
    recertification: Optional[date] = Field(None, description="Recertification date")

class PatientInformation(BaseModel):
    name: Optional[str] = Field(None, description="Patient name, address, and telephone")
    telephone: Optional[str] = Field(None, description="Patient telephone number")
    hicn: Optional[str] = Field(None, description="Health Insurance Claim Number (HICN)")

class SupplierInformation(BaseModel):
    name: Optional[str] = Field(None, description="Supplier name, address, and telephone")
    telephone: Optional[str] = Field(None, description="Supplier telephone number")
    nsc_or_npi: Optional[int] = Field(None, description="Supplier NSC or NPI number")

class AdditionalDetails(BaseModel):
    place_of_service: Optional[str] = Field(None, description="Place of service")
    hcpcs_code: Optional[str] = Field(None, description="HCPCS Code")
    pt_dob: Optional[date] = Field(None, description="Patient date of birth")
    sex: Optional[str] = Field(None, description="Patient sex, M/F")
    height: Optional[int] = Field(None, description="Height in inches")
    weight: Optional[int] = Field(None, description="Weight in pounds")

class FacilityInformation(BaseModel):
    facility_name: Optional[str] = Field(None, description="Name and address of facility")
    physician_name: Optional[str] = Field(None, description="Physician name and address")

class PhysicianInformation(BaseModel):
    nsc_or_npi: Optional[int] = Field(None, description="Physician's NSC or NPI number")
    telephone: Optional[str] = Field(None, description="Physician's telephone number")

class InformationAnswers(BaseModel):
    est_length_of_need: Optional[int] = Field(None, description="Estimated length of need in months")
    diagnosis_codes: Optional[str] = Field(None, description="Diagnosis Codes (ICD-9)")

class Questions(BaseModel):
    question_1: Optional[str] = Field(None, description="Answer to question 1, Y/N/D")
    question_2: Optional[date] = Field(None, description="Answer to question 2 date")
    question_3: Optional[date] = Field(None, description="Answer to question 3 date")
    question_4: Optional[str] = Field(None, description="Answer to question 4, Y/N/D")
    question_5: Optional[int] = Field(None, description="Answer to question 5, number")
    question_6: Optional[str] = Field(None, description="Answer to question 6, Y/N/D")
    question_7: Optional[str] = Field(None, description="Answer to question 7, Y/N/D")
    question_8: Optional[date] = Field(None, description="Answer to question 8 date")
    question_9: Optional[str] = Field(None, description="Answer to question 9, Y/N")
    question_10: Optional[str] = Field(None, description="Answer to question 10, Y/N")

class PersonInformation(BaseModel):
    name: Optional[str] = Field(None, description="Name of person, if not physician")
    title: Optional[str] = Field(None, description="Title of person")
    employer: Optional[str] = Field(None, description="Employer of person")

class PhysicianAttestation(BaseModel):
    signature: Optional[str] = Field(None, description="Physician's signature")
    date: Optional[date] = Field(None, description="Date of physician's signature")

class CertificateOfMedicalNecessity(BaseModel):
    certification_type_date: CertificationTypeDate
    patient_information: PatientInformation
    supplier_information: SupplierInformation
    additional_details: AdditionalDetails
    facility_information: FacilityInformation
    physician_information: PhysicianInformation
    information_answers: InformationAnswers
    questions: Questions
    person_information: Optional[PersonInformation] = None
    physician_attestation: PhysicianAttestation