from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from dotenv import load_dotenv
import time
import json

load_dotenv()
client = OpenAI()

from pydantic import BaseModel, Field
from typing import Optional, List, Literal

class SectionA(BaseModel):
    certification_type: Optional[Literal["INITIAL", "RECERTIFICATION"]] = Field(None, description="Type of certification")
    certification_date: Optional[str] = Field(None, description="Date of certification (MM/DD/YY)")
    patient_name: Optional[str] = Field(None, description="Patient name")
    patient_address: Optional[str] = Field(None, description="Patient address")
    patient_telephone: Optional[str] = Field(None, description="Patient telephone number")
    hicn: Optional[str] = Field(None, description="Health Insurance Claim Number")
    supplier_name: Optional[str] = Field(None, description="Supplier name")
    supplier_address: Optional[str] = Field(None, description="Supplier address")
    supplier_telephone: Optional[str] = Field(None, description="Supplier telephone")
    supplier_nsc_or_npi: Optional[str] = Field(None, description="Supplier NSC or NPI number")
    place_of_service: Optional[str] = Field(None, description="Place of service")
    facility_name_address: Optional[str] = Field(None, description="Name and address of facility if applicable")
    hcpcs_codes: Optional[List[str]] = Field(None, description="List of HCPCS codes")
    patient_dob: Optional[str] = Field(None, description="Patient date of birth (MM/DD/YY)")
    patient_sex: Optional[Literal["M", "F"]] = Field(None, description="Patient sex (M/F)")
    patient_height: Optional[str] = Field(None, description="Patient height in inches")
    patient_weight: Optional[str] = Field(None, description="Patient weight in pounds")
    physician_name: Optional[str] = Field(None, description="Physician name")
    physician_address: Optional[str] = Field(None, description="Physician address")
    physician_nsc_or_npi: Optional[str] = Field(None, description="Physician NSC or NPI number")
    physician_telephone: Optional[str] = Field(None, description="Physician telephone number")

class SectionB(BaseModel):
    estimated_length_of_need: Optional[str] = Field(None, description="Estimated length of need in months (1-99, 99=LIFETIME)")
    diagnosis_codes: Optional[List[str]] = Field(None, description="ICD-9 diagnosis codes")
    
    # Initial evaluation questions (1-7)
    q1_obstructive_sleep_apnea: Optional[Literal["Y", "N"]] = Field(None, description="Is device for obstructive sleep apnea treatment?")
    q2_initial_evaluation_date: Optional[str] = Field(None, description="Date of initial face-to-face evaluation")
    q3_sleep_test_date: Optional[str] = Field(None, description="Date of sleep test")
    q4_facility_based_lab: Optional[Literal["Y", "N"]] = Field(None, description="Was sleep test conducted in facility-based lab?")
    q5_ahi_rdi_index: Optional[str] = Field(None, description="Patient's Apnea-Hypopnea Index (AHI) or Respiratory Disturbance Index (RDI)")
    q6_documented_evidence: Optional[Literal["Y", "N"]] = Field(None, description="Does patient have documented evidence of qualifying symptoms?")
    q7_bilevel_device_tried: Optional[Literal["Y", "N", "D"]] = Field(None, description="If bilevel device ordered, has CPAP been tried and found ineffective?")
    
    # Follow-up evaluation questions (8-10)
    q8_followup_evaluation_date: Optional[str] = Field(None, description="Date of follow-up face-to-face evaluation")
    q9_pap_usage_compliance: Optional[Literal["Y", "N"]] = Field(None, description="Patient used PAP ≥4 hours/night on ≥70% nights in 30 consecutive days?")
    q10_symptom_improvement: Optional[Literal["Y", "N"]] = Field(None, description="Patient demonstrated improvement in OSA symptoms with PAP use?")
    
    # Person answering section B
    answering_person_name: Optional[str] = Field(None, description="Name of person answering Section B questions if other than physician")
    answering_person_title: Optional[str] = Field(None, description="Title of person answering Section B questions")
    answering_person_employer: Optional[str] = Field(None, description="Employer of person answering Section B questions")

class SectionC(BaseModel):
    narrative_description: Optional[str] = Field(None, description="Narrative description of equipment and cost")
    items_and_accessories: Optional[List[str]] = Field(None, description="List of items, accessories and options ordered")
    supplier_charges: Optional[List[str]] = Field(None, description="Supplier's charges for each item")
    medicare_allowances: Optional[List[str]] = Field(None, description="Medicare Fee Schedule Allowance for each item")

class SectionD(BaseModel):
    physician_signature: Optional[str] = Field(None, description="Physician's signature")
    signature_date: Optional[str] = Field(None, description="Date of physician signature")

class PAPDeviceCMN(BaseModel):
    """Certificate of Medical Necessity for Positive Airway Pressure (PAP) Devices for Obstructive Sleep Apnea"""
    section_a: Optional[SectionA] = Field(None, description="Section A: Certification Type/Date and Patient Info")
    section_b: Optional[SectionB] = Field(None, description="Section B: Clinical Information and Questions")
    section_c: Optional[SectionC] = Field(None, description="Section C: Equipment Description and Cost")
    section_d: Optional[SectionD] = Field(None, description="Section D: Physician Attestation and Signature")

transcript = """
Person 1: What type of certification is this?
Person 2: This is an initial certification dated 03/15/2025.
Person 1: Patient information?
Person 2: Robert Martinez, 1234 Oak Street, Columbus OH 43215, phone 614-555-0123, HICN ABC123456789.
Person 1: Supplier details?
Person 2: Sleep Solutions Inc, 5678 Medical Drive, Columbus OH 43220, phone 614-555-0456, NPI 1234567890.
Person 1: Place of service and facility?
Person 2: Place of service is 12 for patient's home. No facility applicable.
Person 1: HCPCS codes?
Person 2: E0601 and E0562.
Person 1: Patient demographics?
Person 2: Date of birth 08/22/1965, male, height 70 inches, weight 220 pounds.
Person 1: Physician information?
Person 2: Dr. Sarah Williams, 9876 Sleep Center Blvd, Columbus OH 43230, NPI 9876543210, phone 614-555-0789.
Person 1: Estimated length of need and diagnosis codes?
Person 2: 99 months for lifetime need. Primary diagnosis code 327.23.
Person 1: Is the device for obstructive sleep apnea treatment?
Person 2: Yes.
Person 1: Date of initial face-to-face evaluation?
Person 2: 02/28/2025.
Person 1: Date of sleep test?
Person 2: 03/01/2025.
Person 1: Was the sleep test conducted in a facility-based lab?
Person 2: Yes.
Person 1: What is the patient's AHI or RDI?
Person 2: AHI is 35 events per hour.
Person 1: Does the patient have documented evidence of qualifying symptoms?
Person 2: Yes, excessive daytime sleepiness and hypertension.
Person 1: If bilevel device is ordered, has CPAP been tried?
Person 2: Does not apply, CPAP device is being ordered.
Person 1: Equipment description and costs?
Person 2: CPAP device with heated humidifier and mask. Supplier charge $800, Medicare allowance $650.
Person 1: Physician signature details?
Person 2: Signed by Dr. Sarah Williams on 03/15/2025.
"""

start_time = time.time()

response = client.responses.parse(
    model="gpt-4.1",
    input=[
        {"role": "system", "content": "Extract the medical information."},
        {
            "role": "user",
            "content": transcript,
        },
    ],
    text_format=PAPDeviceCMN,
)


end_time = time.time()
execution_time = end_time - start_time

result = response.output_parsed

output_data = {
    "execution_time_seconds": execution_time,
    "extracted_medical_data": result.model_dump()
}

# Save to JSON file
with open("medical_extraction_results.json", "w") as f:
    json.dump(output_data, f, indent=2)

print(f"Results saved to medical_extraction_results.json")