from typing import Optional, List
from datetime import date
from pydantic import BaseModel, Field

class CertificationTypeDate(BaseModel):
    initial: Optional[date] = Field(None, description="Initial certification date")
    recertification: Optional[date] = Field(None, description="Recertification date")

class PatientInformation(BaseModel):
    name: Optional[str] = Field(None, description="Patient name, address, telephone, and HICN")
    telephone: Optional[str] = Field(None, description="Patient telephone number")
    hicn: Optional[str] = Field(None, description="Patient Health Insurance Claim Number (HICN)")

class SupplierInformation(BaseModel):
    name: Optional[str] = Field(None, description="Supplier name, address, telephone, and NSC or NPI number")
    telephone: Optional[str] = Field(None, description="Supplier telephone number")
    nsc_or_npi: Optional[int] = Field(None, description="Supplier NSC or NPI number")

class AdditionalDetails(BaseModel):
    place_of_service: Optional[str] = Field(None, description="Place of service")
    hcpcs_code: Optional[str] = Field(None, description="HCPCS code")
    dob: Optional[date] = Field(None, description="Patient date of birth")
    sex: Optional[str] = Field(None, description="Patient sex (M/F)")
    height: Optional[int] = Field(None, description="Patient height in inches")
    weight: Optional[int] = Field(None, description="Patient weight in pounds")

class FacilityInformation(BaseModel):
    name: Optional[str] = Field(None, description="Name and address of facility, if applicable")
    physician_name: Optional[str] = Field(None, description="Physician name and address")

class PhysicianInformation(BaseModel):
    nsc_or_npi: Optional[int] = Field(None, description="Physician's NSC or NPI number")
    telephone: Optional[str] = Field(None, description="Physician's telephone number")

class SectionBInformation(BaseModel):
    length_of_need: Optional[int] = Field(None, description="Estimated length of need in months")
    diagnosis_codes: Optional[str] = Field(None, description="Diagnosis codes (ICD-9)")

class YesNoQuestion(BaseModel):
    response: Optional[str] = Field(None, description="Response to yes/no/does not apply question")

class DateQuestion(BaseModel):
    date: Optional[date] = Field(None, description="Date for question")

class SectionBQuestions(BaseModel):
    question_1: Optional[YesNoQuestion] = Field(None, description="Question 1 response")
    question_2: Optional[DateQuestion] = Field(None, description="Question 2 date")
    question_3: Optional[DateQuestion] = Field(None, description="Question 3 date")
    question_4: Optional[YesNoQuestion] = Field(None, description="Question 4 response")
    question_5: Optional[int] = Field(None, description="Answer for question 5")
    question_6: Optional[YesNoQuestion] = Field(None, description="Question 6 response")
    question_7: Optional[YesNoQuestion] = Field(None, description="Question 7 response")
    question_8: Optional[DateQuestion] = Field(None, description="Question 8 date")
    question_9: Optional[YesNoQuestion] = Field(None, description="Question 9 response")
    question_10: Optional[YesNoQuestion] = Field(None, description="Question 10 response")

class NonPhysicianInformation(BaseModel):
    name: Optional[str] = Field(None, description="Name of person if not physician")
    title: Optional[str] = Field(None, description="Title of person if not physician")
    employer: Optional[str] = Field(None, description="Employer of person if not physician")

class SectionD(BaseModel):
    physician_signature: Optional[str] = Field(None, description="Physician's signature")
    date: Optional[date] = Field(None, description="Date of physician's attestation")

class CertificateOfMedicalNecessityForm(BaseModel):
    certification_type_date: CertificationTypeDate = Field(description="Certification type and date information")
    patient_information: PatientInformation = Field(description="Patient information details")
    supplier_information: SupplierInformation = Field(description="Supplier information details")
    additional_details: AdditionalDetails = Field(description="Additional patient details")
    facility_information: FacilityInformation = Field(description="Facility information if applicable")
    physician_information: PhysicianInformation = Field(description="Physician information details")
    section_b_information: SectionBInformation = Field(description="Section B information")
    questions: SectionBQuestions = Field(description="Section B questions and responses")
    non_physician_information: Optional[NonPhysicianInformation] = Field(None, description="Information of the person, if not the physician")
    section_d: SectionD = Field(description="Physician attestation and signature section")