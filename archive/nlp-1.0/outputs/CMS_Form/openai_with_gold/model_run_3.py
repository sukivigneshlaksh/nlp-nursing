from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class PatientInformation(BaseModel):
    name: Optional[str] = Field(None, description="Patient full name, address, telephone and HICN")
    telephone: Optional[str] = Field(None, description="Patient telephone number")
    hicn: Optional[str] = Field(None, description="Patient HICN")

class SupplierInformation(BaseModel):
    name: Optional[str] = Field(None, description="Supplier name, address, telephone and NSC or NPI #")
    telephone: Optional[str] = Field(None, description="Supplier telephone number")
    nsc_or_npi: Optional[int] = Field(None, description="Supplier NSC or NPI number")

class FacilityInformation(BaseModel):
    name: Optional[str] = Field(None, description="Name and address of facility if applicable")
    physician_name: Optional[str] = Field(None, description="Physician name, address (Printed or Typed)")

class PhysicianInformation(BaseModel):
    nsc_or_npi: Optional[int] = Field(None, description="Physician's NSC or NPI number")
    telephone: Optional[str] = Field(None, description="Physician's telephone number")

class Question(BaseModel):
    question_1: Optional[str] = Field(None, description="Question 1 (Yes/No/Does Not Apply)")
    question_2: Optional[date] = Field(None, description="Question 2 date")
    question_3: Optional[date] = Field(None, description="Question 3 date")
    question_4: Optional[str] = Field(None, description="Question 4 (Yes/No/Does Not Apply)")
    question_5: Optional[int] = Field(None, description="Question 5 number")
    question_6: Optional[str] = Field(None, description="Question 6 (Yes/No/Does Not Apply)")
    question_7: Optional[str] = Field(None, description="Question 7 (Yes/No/Does Not Apply)")
    question_8: Optional[date] = Field(None, description="Question 8 date")
    question_9: Optional[str] = Field(None, description="Question 9 (Yes/No)")
    question_10: Optional[str] = Field(None, description="Question 10 (Yes/No)")

class CertificateOfMedicalNecessity(BaseModel):
    certification_initial_date: Optional[date] = Field(None, description="Initial certification date")
    certification_rec_date: Optional[date] = Field(None, description="Recertification date")
    patient_info: Optional[PatientInformation] = Field(None, description="Patient information")
    supplier_info: Optional[SupplierInformation] = Field(None, description="Supplier information")
    place_of_service: Optional[str] = Field(None, description="Place of service")
    hcpcs_code: Optional[str] = Field(None, description="HCPCS code")
    patient_dob: Optional[date] = Field(None, description="Patient date of birth")
    sex: Optional[str] = Field(None, description="Patient sex (M/F)")
    height: Optional[int] = Field(None, description="Patient height in inches")
    weight: Optional[int] = Field(None, description="Patient weight in pounds")
    facility_info: Optional[FacilityInformation] = Field(None, description="Facility information if applicable")
    physician_info: Optional[PhysicianInformation] = Field(None, description="Physician information")
    length_of_need: Optional[int] = Field(None, description="Estimated length of need in months")
    diagnosis_codes: Optional[str] = Field(None, description="Diagnosis codes (ICD-9)")
    questions: Optional[Question] = Field(None, description="Questions related to the medical necessity")
    name_of_non_physician: Optional[str] = Field(None, description="Name of person if not a physician")
    title_of_non_physician: Optional[str] = Field(None, description="Title of person if not a physician")
    employer_of_non_physician: Optional[str] = Field(None, description="Employer of person if not a physician")
    physician_signature: Optional[str] = Field(None, description="Physician's signature")
    signature_date: Optional[date] = Field(None, description="Date of physician's signature")