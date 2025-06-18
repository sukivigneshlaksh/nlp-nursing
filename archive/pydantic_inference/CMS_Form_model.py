from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from enum import Enum


class PatientInfo(BaseModel):
    """Patient demographic and contact information"""
    patient_telephone: Optional[str] = Field(None, description="(___) ___-____")
    patient_hicn: Optional[str] = Field(None, description="HICN ________________________")
    patient_dob: Optional[date] = Field(None, description="PT DOB ____/____/____")
    patient_sex: Optional[str] = Field(None, description="Sex _____ (M/F)")
    patient_height: Optional[float] = Field(None, description="HT.________(in.)")
    patient_weight: Optional[float] = Field(None, description="WT.______(lbs.)")
    patient_ahi_or_rdi: Optional[float] = Field(None, description="What is the patient's Apnea-Hypopnea Index (AHI) or Respiratory Disturbance Index (RDI)?")
    patient_name: Optional[str] = Field(None, description="Patient’s name")
    patient_dob: Optional[date] = Field(None, description="Patient’s date of birth (MM/DD/YY)")
    patient_sex: Optional[str] = Field(None, description="Sex (male or female)")
    patient_height_inches: Optional[float] = Field(None, description="Height in inches")
    patient_weight_pounds: Optional[float] = Field(None, description="Weight in pounds")

class PhysicianInfo(BaseModel):
    """Physician contact and identification information"""
    physician_name_address: Optional[str] = Field(None, description="PHYSICIAN NAME, ADDRESS (Printed or Typed)")
    physician_npi_or_nsc: Optional[str] = Field(None, description="PHYSICIAN'S NSC or NPI #")
    physician_telephone: Optional[str] = Field(None, description="PHYSICIAN'S TELEPHONE #")
    physician_attestation_signature: Optional[str] = Field(None, description="Physician’s Signature")
    physician_attestation_date: Optional[date] = Field(None, description="Date")
    physician_name: Optional[str] = Field(None, description="Physician Name")
    physician_address: Optional[str] = Field(None, description="Physician Address")
    ordering_physician_npi: Optional[str] = Field(None, description="Accurately indicate the ordering physician’s National Provider Identification number (NPI).")
    physician_telephone_no: Optional[str] = Field(None, description="PHYSICIAN’S TELEPHONE NO: Indicate the telephone number where the physician can be contacted (pre...")
    physician_signature: Optional[str] = Field(None, description="Physician Signature")
    physician_signature_date: Optional[date] = Field(None, description="Date")

class SupplierInfo(BaseModel):
    """Medical equipment supplier information"""
    supplier_telephone: Optional[str] = Field(None, description="(___) ___-____")
    supplier_nsc_or_npi: Optional[str] = Field(None, description="NSC or NPI # ________________________")
    supplier_company_name: Optional[str] = Field(None, description="Name of your company (supplier name)")
    supplier_address: Optional[str] = Field(None, description="Address")
    supplier_telephone_number: Optional[str] = Field(None, description="Telephone number")
    supplier_npi_number: Optional[str] = Field(None, description="National Provider Identification (NPI) number assigned by the National Supplier Clearinghouse (NSC)")

class MedicalInfo(BaseModel):
    """Medical diagnosis and equipment information"""
    hcpcs_code_1: Optional[str] = Field(None, description="HCPCS CODE")
    hcpcs_code_2: Optional[str] = Field(None, description="HCPCS CODE")
    hcpcs_code_3: Optional[str] = Field(None, description="HCPCS CODE")
    hcpcs_code_4: Optional[str] = Field(None, description="HCPCS CODE")
    est_length_of_need_months: Optional[str] = Field(None, description="EST. LENGTH OF NEED (# OF MONTHS): 1–99 (99=LIFETIME)")
    diagnosis_code_1: Optional[str] = Field(None, description="DIAGNOSIS CODE (ICD-9) 1")
    diagnosis_code_2: Optional[str] = Field(None, description="DIAGNOSIS CODE (ICD-9) 2")
    diagnosis_code_3: Optional[str] = Field(None, description="DIAGNOSIS CODE (ICD-9) 3")
    diagnosis_code_4: Optional[str] = Field(None, description="DIAGNOSIS CODE (ICD-9) 4")
    hcpcs_procedure_codes: Optional[str] = Field(None, description="List all HCPCS procedure codes for items ordered that require a CMN.")
    estimated_length_of_need_months: Optional[str] = Field(None, description="Indicate the estimated length of need (the length of time the physician expects the patient to re...")
    primary_icd9_code: Optional[str] = Field(None, description="List the ICD9 code that represents the primary reason for ordering this item.")
    additional_icd9_code_1: Optional[str] = Field(None, description="List any additional ICD9 code to further describe the medical need for the item (code 1 of up to 3).")
    additional_icd9_code_2: Optional[str] = Field(None, description="List any additional ICD9 code to further describe the medical need for the item (code 2 of up to 3).")
    additional_icd9_code_3: Optional[str] = Field(None, description="List any additional ICD9 code to further describe the medical need for the item (code 3 of up to 3).")

class SleepApneaInfo(BaseModel):
    """Sleep apnea specific medical information"""
    device_ordered_for_obstructive_sleep_apnea: Optional[bool] = Field(None, description="Is the device being ordered for the treatment of obstructive sleep apnea (ICD-9 diagnosis code 32...")
    sleep_test_date: Optional[date] = Field(None, description="Enter date of sleep test (If test spans multiple days, enter date of first day of test)")
    sleep_test_conducted_in_facility_lab: Optional[bool] = Field(None, description="Was the patient's sleep test conducted in a facility-based lab?")
    cpap_tried_and_found_ineffective: Optional[str] = Field(None, description="If a bilevel device is ordered, has a CPAP device been tried and found ineffective?")
    pap_usage_documentation: Optional[bool] = Field(None, description="Is there a report documenting that the patient used PAP ≥ 4 hours per night on at least 70% of ni...")
    pap_symptom_improvement: Optional[bool] = Field(None, description="Did the patient demonstrate improvement in symptoms of obstructive sleep apnea with the use of PAP?")

class CertificationInfo(BaseModel):
    """Form certification and signature information"""
    initial_certification_date: Optional[date] = Field(None, description="INITIAL ___/___/___")
    recertification_date: Optional[date] = Field(None, description="RECERTIFICATION ___/___/___")
    initial_face_to_face_evaluation_date: Optional[date] = Field(None, description="Enter date of initial face-to-face evaluation")
    follow_up_face_to_face_evaluation_date: Optional[date] = Field(None, description="Enter date of follow-up face-to-face evaluation")
    initial_date: Optional[date] = Field(None, description="Date needed initially in the space marked “INITIAL” (MM/DD/YY)")
    revised_date: Optional[date] = Field(None, description="Recertification date in the space marked “REVISED” (MM/DD/YY)")
    recertification_date: Optional[date] = Field(None, description="Recertification date in the space marked “RECERTIFICATION” (MM/DD/YY)")
class MedicalEquipmentForm(BaseModel):
    """Complete medical equipment certification form"""
    patient_info: Optional[PatientInfo] = None
    physician_info: Optional[PhysicianInfo] = None
    supplier_info: Optional[SupplierInfo] = None
    medical_info: Optional[MedicalInfo] = None
    sleep_apnea_info: Optional[SleepApneaInfo] = None
    certification_info: Optional[CertificationInfo] = None
    
    # Additional fields from other category
    place_of_service: Optional[str] = Field(None, description="PLACE OF SERVICE")
    facility_name_address: Optional[str] = Field(None, description="NAME and ADDRESS of FACILITY if applicable (See Reverse)")
    documented_evidence_of_comorbid_conditions: Optional[bool] = Field(None, description="Does the patient have documented evidence of at least one of the following? Excessive daytime sle...")
    section_b_responder_name: Optional[str] = Field(None, description="NAME")
    section_b_responder_title: Optional[str] = Field(None, description="TITLE")
    section_b_responder_employer: Optional[str] = Field(None, description="EMPLOYER")
    permanent_legal_address: Optional[str] = Field(None, description="Permanent legal address")
    telephone_number: Optional[str] = Field(None, description="Telephone number")
    health_insurance_claim_number_hicn: Optional[str] = Field(None, description="Health insurance claim number (HICN) as it appears on the Medicare card and on the claim form")
    place_of_service: Optional[str] = Field(None, description="Place of Service: Indicate the place in which the item is being used, i.e., patient’s home is 12,...")
    facility_name_and_address: Optional[str] = Field(None, description="If the place of service is a facility, indicate the name and complete address of the facility.")
    name_of_person_answering_section_b: Optional[str] = Field(None, description="NAME OF PERSON ANSWERING SECTION B QUESTIONS")