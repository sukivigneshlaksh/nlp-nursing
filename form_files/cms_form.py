from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class CertificationType(str, Enum):
    initial = "Initial"
    recertification = "Recertification"

class Sex(str, Enum):
    male = "M"
    female = "F"

class YesNoDoesNotApply(str, Enum):
    yes = "Y"
    no = "N"
    does_not_apply = "D"

class YesNo(str, Enum):
    yes = "Y"
    no = "N"

class PatientInfo(BaseModel):
    name: Optional[str] = Field(None, description="Patient's full name")
    address: Optional[str] = Field(None, description="Patient's address")
    telephone: Optional[str] = Field(None, description="Patient's telephone number")
    hicn: Optional[str] = Field(None, description="Health Insurance Claim Number")
    date_of_birth: Optional[str] = Field(None, description="Patient's date of birth")
    sex: Optional[Sex] = Field(None, description="Patient's sex (M/F)")
    height_inches: Optional[int] = Field(None, description="Patient's height in inches")
    weight_pounds: Optional[int] = Field(None, description="Patient's weight in pounds")

class SupplierInfo(BaseModel):
    name: Optional[str] = Field(None, description="Supplier company name")
    address: Optional[str] = Field(None, description="Supplier address")
    telephone: Optional[str] = Field(None, description="Supplier telephone number")
    nsc_or_npi: Optional[str] = Field(None, description="NSC or NPI number")

class PhysicianInfo(BaseModel):
    name: Optional[str] = Field(None, description="Physician's name")
    address: Optional[str] = Field(None, description="Physician's address")
    nsc_or_npi: Optional[str] = Field(None, description="Physician's NSC or NPI number")
    telephone: Optional[str] = Field(None, description="Physician's telephone number")

class ClinicalQuestions(BaseModel):
    # Initial evaluation questions (1-7)
    obstructive_sleep_apnea_treatment: Optional[YesNo] = Field(None, description="Is device being ordered for treatment of obstructive sleep apnea (ICD-9 327.23)?")
    initial_face_to_face_date: Optional[str] = Field(None, description="Date of initial face-to-face evaluation")
    sleep_test_date: Optional[str] = Field(None, description="Date of sleep test")
    facility_based_sleep_test: Optional[YesNo] = Field(None, description="Was patient's sleep test conducted in facility-based lab?")
    ahi_or_rdi_value: Optional[str] = Field(None, description="Patient's Apnea-Hypopnea Index (AHI) or Respiratory Disturbance Index (RDI)")
    documented_symptoms: Optional[YesNo] = Field(None, description="Does patient have documented evidence of excessive daytime sleepiness, impaired cognition, mood disorders, insomnia, hypertension, ischemic heart disease or history of stroke?")
    bilevel_cpap_ineffective: Optional[YesNoDoesNotApply] = Field(None, description="If bilevel device ordered, has CPAP device been tried and found ineffective?")
    
    # Follow-up evaluation questions (8-10)
    followup_face_to_face_date: Optional[str] = Field(None, description="Date of follow-up face-to-face evaluation")
    pap_usage_compliance: Optional[YesNo] = Field(None, description="Is there report documenting patient used PAP ≥4 hours per night on at least 70% of nights in 30 consecutive day period?")
    symptom_improvement: Optional[YesNo] = Field(None, description="Did patient demonstrate improvement in symptoms of obstructive sleep apnea with use of PAP?")

class PersonAnswering(BaseModel):
    name: Optional[str] = Field(None, description="Name of person answering Section B questions if other than physician")
    title: Optional[str] = Field(None, description="Professional title of person answering questions")
    employer: Optional[str] = Field(None, description="Employer of person answering questions")

class CMSPAPDeviceForm(BaseModel):
    """CMS Certificate of Medical Necessity for PAP Devices form data"""
    
    # Section A
    certification_type: Optional[CertificationType] = Field(None, description="Type of certification (Initial or Recertification)")
    certification_date: Optional[str] = Field(None, description="Date of certification")
    patient_info: Optional[PatientInfo] = Field(None, description="Patient information")
    supplier_info: Optional[SupplierInfo] = Field(None, description="Supplier information")
    physician_info: Optional[PhysicianInfo] = Field(None, description="Physician information")
    place_of_service: Optional[str] = Field(None, description="Place where item is being used")
    facility_name: Optional[str] = Field(None, description="Name of facility if applicable")
    hcpcs_codes: Optional[List[str]] = Field(None, description="HCPCS procedure codes for items ordered")
    
    # Section B
    estimated_length_of_need: Optional[int] = Field(None, description="Estimated length of need in months (99=lifetime)")
    diagnosis_codes: Optional[List[str]] = Field(None, description="ICD-9 diagnosis codes")
    clinical_questions: Optional[ClinicalQuestions] = Field(None, description="Clinical evaluation questions")
    person_answering: Optional[PersonAnswering] = Field(None, description="Person answering Section B if not physician")
    
    # Section C
    equipment_description: Optional[str] = Field(None, description="Narrative description of equipment and cost")
    
    # Section D
    physician_signature_date: Optional[str] = Field(None, description="Date of physician signature")

# Sample transcript for CMS PAP Device form
sample_cms_transcript = """
CMS PAP DEVICE CERTIFICATION INTERVIEW
Date: June 18, 2025

MEDICAL ASSISTANT: I need to complete the CMS Certificate of Medical Necessity for your PAP device. Let me gather the required information.

MEDICAL ASSISTANT: This is an initial certification, correct?
PATIENT: Yes, this is my first time getting a CPAP machine.

MEDICAL ASSISTANT: Let me confirm your information. Your name is Robert Williams, correct?
PATIENT: Yes, that's right. Robert J. Williams.

MEDICAL ASSISTANT: Your address is 1234 Main Street, Columbus, Ohio 43215?
PATIENT: Yes, that's correct.

MEDICAL ASSISTANT: Phone number is 614-555-0123?
PATIENT: Yes.

MEDICAL ASSISTANT: Your Medicare number is 1EG4-TE5-MK72?
PATIENT: That sounds right.

MEDICAL ASSISTANT: Date of birth is March 15, 1965?
PATIENT: Correct, I'm 60 years old.

MEDICAL ASSISTANT: You're male, height 5 foot 10 inches, weight 210 pounds?
PATIENT: Yes, that's all correct.

MEDICAL ASSISTANT: Dr. Peterson is your ordering physician at Sleep Medicine Associates, 567 Medical Drive, Columbus, Ohio 43220, phone 614-555-7890?
PATIENT: Yes, that's my sleep doctor.

MEDICAL ASSISTANT: Now for the clinical questions. Is this device being ordered for treatment of obstructive sleep apnea?
PATIENT: Yes, that's what Dr. Peterson diagnosed me with.

MEDICAL ASSISTANT: Your initial face-to-face evaluation with Dr. Peterson was on May 20, 2025?
PATIENT: Yes, that was my first appointment.

MEDICAL ASSISTANT: Your sleep study was conducted on June 1, 2025?
PATIENT: Yes, I spent the night at the sleep lab.

MEDICAL ASSISTANT: Was your sleep test conducted in a facility-based lab?
PATIENT: Yes, I went to the Columbus Sleep Center overnight.

MEDICAL ASSISTANT: Your sleep study showed an AHI of 35 events per hour?
PATIENT: Yes, Dr. Peterson said that was severe sleep apnea.

MEDICAL ASSISTANT: Do you have documented symptoms like excessive daytime sleepiness, mood issues, or high blood pressure?
PATIENT: Yes, I have high blood pressure and I'm constantly tired during the day. I fall asleep at work sometimes.

MEDICAL ASSISTANT: Since we're ordering a standard CPAP device, not a bilevel, this question doesn't apply to you.
PATIENT: Okay.

MEDICAL ASSISTANT: The equipment being ordered is a ResMed AirSense 10 CPAP machine with heated humidifier and full face mask.
PATIENT: That's what Dr. Peterson recommended.

MEDICAL ASSISTANT: The estimated length of need is lifetime, which we code as 99 months.
PATIENT: Dr. Peterson said I'll need this permanently.

MEDICAL ASSISTANT: The primary diagnosis code is 327.23 for obstructive sleep apnea, with secondary code 401.9 for hypertension.
PATIENT: That matches what Dr. Peterson told me.

MEDICAL ASSISTANT: Dr. Peterson will review and sign this form to certify the medical necessity.
PATIENT: Perfect, when can I get the machine?
"""