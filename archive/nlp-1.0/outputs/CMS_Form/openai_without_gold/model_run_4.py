from typing import Optional, List
from datetime import date
from pydantic import BaseModel, Field

class ContactInfo(BaseModel):
    name: Optional[str] = Field(None, description="Full name")
    address: Optional[str] = Field(None, description="Mailing address")
    telephone: Optional[str] = Field(None, description="Telephone number")

class FacilityInfo(BaseModel):
    name: Optional[str] = Field(None, description="Name of facility")
    address: Optional[str] = Field(None, description="Address of facility")

class PhysicianInfo(BaseModel):
    name: Optional[str] = Field(None, description="Physician full name")
    npi: Optional[int] = Field(None, description="Physician NSC or NPI number")
    telephone: Optional[str] = Field(None, description="Physician telephone number")

class CertificationTypeDate(BaseModel):
    initial_date: Optional[date] = Field(None, description="Date of initial certification")
    recertification_date: Optional[date] = Field(None, description="Date of recertification")

class SectionA(BaseModel):
    certification: CertificationTypeDate
    patient_info: ContactInfo
    supplier_info: ContactInfo
    npi: Optional[int] = Field(None, description="Supplier NSC or NPI number")

class AdditionalDetails(BaseModel):
    place_of_service: Optional[str] = Field(None, description="Place of service")
    hcpcs_code: Optional[str] = Field(None, description="HCPCS code")
    dob: Optional[date] = Field(None, description="Patient date of birth")
    sex: Optional[str] = Field(None, description="Patient sex ('M' or 'F')")
    height: Optional[int] = Field(None, description="Patient height in inches")
    weight: Optional[int] = Field(None, description="Patient weight in pounds")

class SectionBQuestions(BaseModel):
    question_1: Optional[str] = Field(None, description="Answer to Question 1 (Y/N/D)")
    date_2: Optional[date] = Field(None, description="Date for Question 2")
    date_3: Optional[date] = Field(None, description="Date for Question 3")
    question_4: Optional[str] = Field(None, description="Answer to Question 4 (Y/N/D)")
    value_5: Optional[int] = Field(None, description="Value for Question 5")
    question_6: Optional[str] = Field(None, description="Answer to Question 6 (Y/N/D)")
    question_7: Optional[str] = Field(None, description="Answer to Question 7 (Y/N/D)")
    date_8: Optional[date] = Field(None, description="Date for Question 8")
    question_9: Optional[str] = Field(None, description="Answer to Question 9 (Y/N)")
    question_10: Optional[str] = Field(None, description="Answer to Question 10 (Y/N)")

class SectionBInformation(BaseModel):
    length_of_need: Optional[int] = Field(None, description="Estimated length of need in months")
    diagnosis_codes: Optional[str] = Field(None, description="Diagnosis codes (ICD-9)")
    questions: SectionBQuestions

class PersonIfNotPhysician(BaseModel):
    name: Optional[str] = Field(None, description="Full name of person other than physician")
    title: Optional[str] = Field(None, description="Title of the person")
    employer: Optional[str] = Field(None, description="Employer of the person")

class SectionD(BaseModel):
    signature: Optional[str] = Field(None, description="Physician's signature")
    date: Optional[date] = Field(None, description="Date of signature")

class CertificateOfMedicalNecessity(BaseModel):
    section_a: SectionA
    additional_details: AdditionalDetails
    facility_info: FacilityInfo
    physician_info: PhysicianInfo
    section_b: SectionBInformation
    person_if_not_physician: PersonIfNotPhysician
    section_d: SectionD