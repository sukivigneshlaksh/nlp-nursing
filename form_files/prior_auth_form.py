from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class YesNo(str, Enum):
    yes = "Yes"
    no = "No"

class NewContinuation(str, Enum):
    new = "New"
    continuation = "Continuation of Therapy"

class MedicationAdministered(str, Enum):
    self_administered = "Self-Administered"
    physicians_office = "Physician's Office"
    other = "Other"

class MemberInfo(BaseModel):
    name: Optional[str] = Field(None, description="Member's full name")
    member_id: Optional[str] = Field(None, description="Member ID number")
    date_of_birth: Optional[str] = Field(None, description="Member's date of birth")
    street_address: Optional[str] = Field(None, description="Member's street address")
    city: Optional[str] = Field(None, description="Member's city")
    state: Optional[str] = Field(None, description="Member's state")
    zip_code: Optional[str] = Field(None, description="Member's ZIP code")
    phone: Optional[str] = Field(None, description="Member's phone number")
    allergies: Optional[str] = Field(None, description="Member's allergies")

class PrescriberInfo(BaseModel):
    provider_name: Optional[str] = Field(None, description="Provider's name")
    npi_number: Optional[str] = Field(None, description="Provider's NPI number")
    specialty: Optional[str] = Field(None, description="Provider's medical specialty")
    office_phone: Optional[str] = Field(None, description="Provider's office phone")
    office_fax: Optional[str] = Field(None, description="Provider's office fax")
    office_street_address: Optional[str] = Field(None, description="Provider's office street address")
    office_city: Optional[str] = Field(None, description="Provider's office city")
    office_state: Optional[str] = Field(None, description="Provider's office state")
    office_zip_code: Optional[str] = Field(None, description="Provider's office ZIP code")

class MedicationInfo(BaseModel):
    medication_name: Optional[str] = Field(None, description="Name of the medication")
    strength: Optional[str] = Field(None, description="Strength of the medication")
    directions_for_use: Optional[str] = Field(None, description="Directions for medication use")
    quantity: Optional[str] = Field(None, description="Quantity of medication")
    medication_administered: Optional[MedicationAdministered] = Field(None, description="How medication is administered")
    administration_other: Optional[str] = Field(None, description="Other administration method if not self-administered or physician's office")

class ClinicalInfo(BaseModel):
    diagnosis: Optional[str] = Field(None, description="Patient's diagnosis for the requested medication")
    icd10_codes: Optional[List[str]] = Field(None, description="ICD-10 diagnosis codes")
    medication_failures: Optional[str] = Field(None, description="Medications patient has history of failure to, including strengths, directions, length of trial, and reason for discontinuation")
    contraindications_intolerances: Optional[str] = Field(None, description="Medications patient has contraindication or intolerance to, with specific issues")
    lab_test_results: Optional[str] = Field(None, description="Supporting laboratory or test results related to diagnosis")
    additional_information: Optional[str] = Field(None, description="Additional information important for review")

class PriorAuthForm(BaseModel):
    """UnitedHealthcare Prior Authorization Request Form data"""
    
    # Member and prescriber information
    member_info: Optional[MemberInfo] = Field(None, description="Member information")
    prescriber_info: Optional[PrescriberInfo] = Field(None, description="Prescriber information")
    
    # Request details
    medication_type: Optional[NewContinuation] = Field(None, description="Is requested medication new or continuation of therapy")
    therapy_start_date: Optional[str] = Field(None, description="Start date if continuation of therapy")
    currently_hospitalized: Optional[YesNo] = Field(None, description="Is patient currently hospitalized")
    discharge_date: Optional[str] = Field(None, description="Discharge date if recently discharged")
    member_pregnant: Optional[YesNo] = Field(None, description="Is member pregnant")
    due_date: Optional[str] = Field(None, description="Due date if member is pregnant")
    
    # Medication information
    medication_info: Optional[MedicationInfo] = Field(None, description="Medication information")
    
    # Clinical information
    clinical_info: Optional[ClinicalInfo] = Field(None, description="Clinical information")
    
    # Provider signature
    provider_signature_date: Optional[str] = Field(None, description="Date of provider signature")

# Sample transcript for Prior Authorization form
sample_prior_auth_transcript = """
PRIOR AUTHORIZATION REQUEST INTERVIEW
Date: June 18, 2025

PHARMACY TECHNICIAN: I need to complete a prior authorization request for your medication. Let me gather the required information.

PHARMACY TECHNICIAN: Can you confirm the member information? The name is Lisa Thompson?
PATIENT: Yes, that's correct.

PHARMACY TECHNICIAN: Member ID is UHC123456789?
PATIENT: Yes, that's right.

PHARMACY TECHNICIAN: Date of birth is April 22, 1978?
PATIENT: Correct.

PHARMACY TECHNICIAN: Address is 789 Oak Street, Columbus, Ohio 43215?
PATIENT: Yes, that's my address.

PHARMACY TECHNICIAN: Phone number is 614-555-4567?
PATIENT: Yes.

PHARMACY TECHNICIAN: Any known allergies?
PATIENT: I'm allergic to penicillin and sulfa drugs.

PHARMACY TECHNICIAN: Your prescribing doctor is Dr. Jennifer Martinez at Endocrinology Associates?
PATIENT: Yes, she's my endocrinologist.

PHARMACY TECHNICIAN: Her NPI number is 1234567890, office phone 614-555-8900, fax 614-555-8901?
PATIENT: That sounds right.

PHARMACY TECHNICIAN: Office address is 456 Medical Plaza, Columbus, Ohio 43220?
PATIENT: Yes, that's her office.

PHARMACY TECHNICIAN: The medication being requested is Ozempic, 1mg pen?
PATIENT: Yes, that's what Dr. Martinez prescribed.

PHARMACY TECHNICIAN: This is a new medication for you, not a continuation?
PATIENT: Yes, this is the first time I'm trying Ozempic.

PHARMACY TECHNICIAN: You're not currently hospitalized?
PATIENT: No, I'm not in the hospital.

PHARMACY TECHNICIAN: Are you pregnant?
PATIENT: No, I'm not pregnant.

PHARMACY TECHNICIAN: The directions are to inject 1mg subcutaneously once weekly?
PATIENT: Yes, once a week injection.

PHARMACY TECHNICIAN: Quantity is a 30-day supply, which is 4 pens?
PATIENT: That's what the prescription says.

PHARMACY TECHNICIAN: This is self-administered at home?
PATIENT: Yes, I'll give myself the injections.

PHARMACY TECHNICIAN: The diagnosis is Type 2 diabetes mellitus?
PATIENT: Yes, that's what Dr. Martinez diagnosed me with.

PHARMACY TECHNICIAN: The ICD-10 code is E11.9 for Type 2 diabetes without complications?
PATIENT: I think so, that's what she mentioned.

PHARMACY TECHNICIAN: Have you tried other diabetes medications before that didn't work?
PATIENT: Yes, I tried metformin for 6 months but it caused severe stomach upset and diarrhea. Then I tried glipizide for 3 months but my blood sugar wasn't well controlled.

PHARMACY TECHNICIAN: Any medications you can't take due to allergies or other reasons?
PATIENT: Besides the penicillin and sulfa allergy I mentioned, I can't take metformin because of the GI side effects.

PHARMACY TECHNICIAN: Any recent lab results related to your diabetes?
PATIENT: Dr. Martinez ordered an A1C last week and it came back at 9.2%, which is why she wants to start the Ozempic.

PHARMACY TECHNICIAN: Any other information that might be important?
PATIENT: My blood sugar has been running 200-300 despite diet and exercise. Dr. Martinez said this medication might help with weight loss too, which would be beneficial.

PHARMACY TECHNICIAN: Dr. Martinez will need to sign this form, and we should have a decision within 24 hours.
PATIENT: Perfect, I really hope this gets approved.
"""