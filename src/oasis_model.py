from pydantic import BaseModel, Field, validator
from typing import Optional, List, Literal, Union
from datetime import date
from enum import Enum

# Enums for coded values
class GenderCode(str, Enum):
    MALE = "1"
    FEMALE = "2"

class EthnicityCode(str, Enum):
    NOT_HISPANIC = "A"
    MEXICAN = "B"
    PUERTO_RICAN = "C"
    CUBAN = "D"
    OTHER_HISPANIC = "E"
    UNABLE_TO_RESPOND = "X"
    DECLINES_TO_RESPOND = "Y"

class RaceCode(str, Enum):
    WHITE = "A"
    BLACK_AFRICAN_AMERICAN = "B"
    AMERICAN_INDIAN_ALASKA_NATIVE = "C"
    ASIAN_INDIAN = "D"
    CHINESE = "E"
    FILIPINO = "F"
    JAPANESE = "G"
    KOREAN = "H"
    VIETNAMESE = "I"
    OTHER_ASIAN = "J"
    NATIVE_HAWAIIAN = "K"
    GUAMANIAN_CHAMORRO = "L"
    SAMOAN = "M"
    OTHER_PACIFIC_ISLANDER = "N"
    UNABLE_TO_RESPOND = "X"
    DECLINES_TO_RESPOND = "Y"
    NONE_OF_ABOVE = "Z"

class PaymentSourceCode(str, Enum):
    NONE = "0"
    MEDICARE_TRADITIONAL = "1"
    MEDICARE_HMO = "2"
    MEDICAID_TRADITIONAL = "3"
    MEDICAID_HMO = "4"
    WORKERS_COMP = "5"
    TITLE_PROGRAMS = "6"
    OTHER_GOVERNMENT = "7"
    PRIVATE_INSURANCE = "8"
    PRIVATE_HMO = "9"
    SELF_PAY = "10"
    OTHER = "11"
    UNKNOWN = "UK"

class DisciplineCode(str, Enum):
    RN = "1"
    PT = "2"
    SLP_ST = "3"
    OT = "4"

class AssessmentReasonCode(str, Enum):
    START_OF_CARE = "1"
    RESUMPTION_OF_CARE = "3"
    RECERTIFICATION = "4"
    OTHER_FOLLOWUP = "5"
    TRANSFER_NOT_DISCHARGED = "6"
    TRANSFER_DISCHARGED = "7"
    DEATH_AT_HOME = "8"
    DISCHARGE_FROM_AGENCY = "9"

class HearingCode(str, Enum):
    ADEQUATE = "0"
    MINIMAL_DIFFICULTY = "1"
    MODERATE_DIFFICULTY = "2"
    HIGHLY_IMPAIRED = "3"

class VisionCode(str, Enum):
    ADEQUATE = "0"
    IMPAIRED = "1"
    MODERATELY_IMPAIRED = "2"
    HIGHLY_IMPAIRED = "3"
    SEVERELY_IMPAIRED = "4"

class CognitiveFunctioningCode(str, Enum):
    ALERT_ORIENTED = "0"
    REQUIRES_PROMPTING = "1"
    REQUIRES_ASSISTANCE = "2"
    CONSIDERABLE_ASSISTANCE = "3"
    TOTALLY_DEPENDENT = "4"

class FunctionalAbilityCode(str, Enum):
    INDEPENDENT = "06"
    SETUP_CLEANUP = "05"
    SUPERVISION_TOUCHING = "04"
    PARTIAL_MODERATE = "03"
    SUBSTANTIAL_MAXIMAL = "02"
    DEPENDENT = "01"
    REFUSED = "07"
    NOT_APPLICABLE = "09"
    NOT_ATTEMPTED_ENVIRONMENTAL = "10"
    NOT_ATTEMPTED_MEDICAL = "88"

# Data Models
class AdministrativeInfo(BaseModel):
    npi_attending_physician: Optional[str] = Field(None, description="M0018 - National Provider Identifier")
    cms_certification_number: Optional[str] = Field(None, description="M0010")
    branch_state: Optional[str] = Field(None, description="M0014")
    branch_id: Optional[str] = Field(None, description="M0016")
    patient_id: Optional[str] = Field(None, description="M0020")
    start_of_care_date: Optional[date] = Field(None, description="M0030")
    resumption_of_care_date: Optional[date] = Field(None, description="M0032")
    patient_first_name: Optional[str] = Field(None, description="M0040")
    patient_middle_initial: Optional[str] = Field(None, description="M0040")
    patient_last_name: Optional[str] = Field(None, description="M0040")
    patient_suffix: Optional[str] = Field(None, description="M0040")
    patient_state_of_residence: Optional[str] = Field(None, description="M0050")
    patient_zip_code: Optional[str] = Field(None, description="M0060")
    social_security_number: Optional[str] = Field(None, description="M0064")
    medicare_number: Optional[str] = Field(None, description="M0063")
    medicaid_number: Optional[str] = Field(None, description="M0065")
    gender: Optional[GenderCode] = Field(None, description="M0069")
    birth_date: Optional[date] = Field(None, description="M0066")
    ethnicity: List[EthnicityCode] = Field(default_factory=list, description="A1005")
    race: List[RaceCode] = Field(default_factory=list, description="A1010")
    payment_sources: List[PaymentSourceCode] = Field(default_factory=list, description="M0150")
    preferred_language: Optional[str] = Field(None, description="A1110")
    needs_interpreter: Optional[Literal["0", "1", "9"]] = Field(None, description="A1110")
    assessment_discipline: Optional[DisciplineCode] = Field(None, description="M0080")
    assessment_date: Optional[date] = Field(None, description="M0090")
    assessment_reason: Optional[AssessmentReasonCode] = Field(None, description="M0100")

class SensoryCapabilities(BaseModel):
    hearing: Optional[HearingCode] = Field(None, description="B0200")
    vision: Optional[VisionCode] = Field(None, description="B1000")
    health_literacy: Optional[Literal["0", "1", "2", "3", "4", "7", "8"]] = Field(None, description="B1300")

class CognitiveBehavioralAssessment(BaseModel):
    brief_interview_conducted: Optional[Literal["0", "1"]] = Field(None, description="C0100")
    word_repetition_score: Optional[Literal["0", "1", "2", "3"]] = Field(None, description="C0200")
    temporal_orientation_year: Optional[Literal["0", "1", "2", "3"]] = Field(None, description="C0300A")
    temporal_orientation_month: Optional[Literal["0", "1", "2"]] = Field(None, description="C0300B")
    temporal_orientation_day: Optional[Literal["0", "1"]] = Field(None, description="C0300C")
    recall_sock: Optional[Literal["0", "1", "2"]] = Field(None, description="C0400A")
    recall_blue: Optional[Literal["0", "1", "2"]] = Field(None, description="C0400B")
    recall_bed: Optional[Literal["0", "1", "2"]] = Field(None, description="C0400C")
    bims_summary_score: Optional[int] = Field(None, ge=0, le=15, description="C0500")
    cognitive_functioning: Optional[CognitiveFunctioningCode] = Field(None, description="M1700")
    when_confused: Optional[Literal["0", "1", "2", "3", "4", "NA"]] = Field(None, description="M1710")
    when_anxious: Optional[Literal["0", "1", "2", "3", "NA"]] = Field(None, description="M1720")

class MoodAssessment(BaseModel):
    phq2_interest_presence: Optional[Literal["0", "1", "9"]] = Field(None, description="D0150A1")
    phq2_interest_frequency: Optional[Literal["0", "1", "2", "3"]] = Field(None, description="D0150A2")
    phq2_mood_presence: Optional[Literal["0", "1", "9"]] = Field(None, description="D0150B1")
    phq2_mood_frequency: Optional[Literal["0", "1", "2", "3"]] = Field(None, description="D0150B2")
    total_severity_score: Optional[int] = Field(None, ge=0, le=27, description="D0160")
    social_isolation: Optional[Literal["0", "1", "2", "3", "4", "7", "8"]] = Field(None, description="D0700")

class FunctionalStatus(BaseModel):
    grooming: Optional[Literal["0", "1", "2", "3"]] = Field(None, description="M1800")
    upper_body_dressing: Optional[Literal["0", "1", "2", "3"]] = Field(None, description="M1810")
    lower_body_dressing: Optional[Literal["0", "1", "2", "3"]] = Field(None, description="M1820")
    bathing: Optional[Literal["0", "1", "2", "3", "4", "5", "6"]] = Field(None, description="M1830")
    toilet_transferring: Optional[Literal["0", "1", "2", "3", "4"]] = Field(None, description="M1840")
    toileting_hygiene: Optional[Literal["0", "1", "2", "3"]] = Field(None, description="M1845")
    transferring: Optional[Literal["0", "1", "2", "3", "4", "5"]] = Field(None, description="M1850")
    ambulation: Optional[Literal["0", "1", "2", "3", "4", "5", "6"]] = Field(None, description="M1860")

class SelfCareAssessment(BaseModel):
    eating_soc: Optional[FunctionalAbilityCode] = Field(None, description="GG0130A SOC/ROC")
    eating_followup: Optional[FunctionalAbilityCode] = Field(None, description="GG0130A Follow-up")
    eating_discharge: Optional[FunctionalAbilityCode] = Field(None, description="GG0130A Discharge")
    oral_hygiene_soc: Optional[FunctionalAbilityCode] = Field(None, description="GG0130B SOC/ROC")
    oral_hygiene_followup: Optional[FunctionalAbilityCode] = Field(None, description="GG0130B Follow-up")
    oral_hygiene_discharge: Optional[FunctionalAbilityCode] = Field(None, description="GG0130B Discharge")
    toileting_hygiene_soc: Optional[FunctionalAbilityCode] = Field(None, description="GG0130C SOC/ROC")
    toileting_hygiene_followup: Optional[FunctionalAbilityCode] = Field(None, description="GG0130C Follow-up")
    toileting_hygiene_discharge: Optional[FunctionalAbilityCode] = Field(None, description="GG0130C Discharge")
    showering_soc: Optional[FunctionalAbilityCode] = Field(None, description="GG0130E SOC/ROC")
    showering_discharge: Optional[FunctionalAbilityCode] = Field(None, description="GG0130E Discharge")
    upper_body_dressing_soc: Optional[FunctionalAbilityCode] = Field(None, description="GG0130F SOC/ROC")
    upper_body_dressing_discharge: Optional[FunctionalAbilityCode] = Field(None, description="GG0130F Discharge")
    lower_body_dressing_soc: Optional[FunctionalAbilityCode] = Field(None, description="GG0130G SOC/ROC")
    lower_body_dressing_discharge: Optional[FunctionalAbilityCode] = Field(None, description="GG0130G Discharge")
    footwear_soc: Optional[FunctionalAbilityCode] = Field(None, description="GG0130H SOC/ROC")
    footwear_discharge: Optional[FunctionalAbilityCode] = Field(None, description="GG0130H Discharge")

class MobilityAssessment(BaseModel):
    roll_left_right_soc: Optional[FunctionalAbilityCode] = Field(None, description="GG0170A SOC/ROC")
    roll_left_right_followup: Optional[FunctionalAbilityCode] = Field(None, description="GG0170A Follow-up")
    roll_left_right_discharge: Optional[FunctionalAbilityCode] = Field(None, description="GG0170A Discharge")
    sit_to_lying_soc: Optional[FunctionalAbilityCode] = Field(None, description="GG0170B SOC/ROC")
    sit_to_lying_followup: Optional[FunctionalAbilityCode] = Field(None, description="GG0170B Follow-up")
    sit_to_lying_discharge: Optional[FunctionalAbilityCode] = Field(None, description="GG0170B Discharge")
    lying_to_sitting_soc: Optional[FunctionalAbilityCode] = Field(None, description="GG0170C SOC/ROC")
    lying_to_sitting_followup: Optional[FunctionalAbilityCode] = Field(None, description="GG0170C Follow-up")
    lying_to_sitting_discharge: Optional[FunctionalAbilityCode] = Field(None, description="GG0170C Discharge")
    sit_to_stand_soc: Optional[FunctionalAbilityCode] = Field(None, description="GG0170D SOC/ROC")
    sit_to_stand_followup: Optional[FunctionalAbilityCode] = Field(None, description="GG0170D Follow-up")
    sit_to_stand_discharge: Optional[FunctionalAbilityCode] = Field(None, description="GG0170D Discharge")
    walk_10_feet_soc: Optional[FunctionalAbilityCode] = Field(None, description="GG0170I SOC/ROC")
    walk_10_feet_followup: Optional[FunctionalAbilityCode] = Field(None, description="GG0170I Follow-up")
    walk_10_feet_discharge: Optional[FunctionalAbilityCode] = Field(None, description="GG0170I Discharge")
    walk_50_feet_turns_soc: Optional[FunctionalAbilityCode] = Field(None, description="GG0170J SOC/ROC")
    walk_50_feet_turns_discharge: Optional[FunctionalAbilityCode] = Field(None, description="GG0170J Discharge")
    walk_150_feet_soc: Optional[FunctionalAbilityCode] = Field(None, description="GG0170K SOC/ROC")
    walk_150_feet_discharge: Optional[FunctionalAbilityCode] = Field(None, description="GG0170K Discharge")

class HealthConditions(BaseModel):
    uti_treated_past_14_days: Optional[Literal["0", "1", "NA", "UK"]] = Field(None, description="M1600")
    urinary_incontinence: Optional[Literal["0", "1", "2"]] = Field(None, description="M1610")
    bowel_incontinence_frequency: Optional[Literal["0", "1", "2", "3", "4", "5", "NA", "UK"]] = Field(None, description="M1620")
    shortness_of_breath: Optional[Literal["0", "1", "2", "3", "4"]] = Field(None, description="M1400")
    pain_effect_on_sleep: Optional[Literal["0", "1", "2", "3", "4", "8"]] = Field(None, description="J0510")
    pain_therapy_interference: Optional[Literal["0", "1", "2", "3", "4", "8"]] = Field(None, description="J0520")
    pain_daily_interference: Optional[Literal["1", "2", "3", "4", "8"]] = Field(None, description="J0530")

class Medications(BaseModel):
    oral_medication_management: Optional[Literal["0", "1", "2", "3", "NA"]] = Field(None, description="M2020")
    injectable_medication_management: Optional[Literal["0", "1", "2", "3", "NA"]] = Field(None, description="M2030")
    drug_regimen_review_issues: Optional[Literal["0", "1", "9"]] = Field(None, description="M2001")
    high_risk_drugs_antipsychotic: bool = Field(False, description="N0415A1")
    high_risk_drugs_anticoagulant: bool = Field(False, description="N0415E1")
    high_risk_drugs_antibiotic: bool = Field(False, description="N0415F1")
    high_risk_drugs_opioid: bool = Field(False, description="N0415H1")
    high_risk_drugs_antiplatelet: bool = Field(False, description="N0415I1")
    high_risk_drugs_hypoglycemic: bool = Field(False, description="N0415J1")

class SkinConditions(BaseModel):
    unhealed_pressure_ulcer_stage2_higher: Optional[Literal["0", "1"]] = Field(None, description="M1306")
    stage1_pressure_injuries: Optional[Literal["0", "1", "2", "3", "4"]] = Field(None, description="M1322")
    most_problematic_ulcer_stage: Optional[Literal["1", "2", "3", "4", "NA"]] = Field(None, description="M1324")
    has_stasis_ulcer: Optional[Literal["0", "1", "2", "3"]] = Field(None, description="M1330")
    has_surgical_wound: Optional[Literal["0", "1", "2"]] = Field(None, description="M1340")

class NutritionalStatus(BaseModel):
    height_inches: Optional[int] = Field(None, description="M1060A")
    weight_pounds: Optional[int] = Field(None, description="M1060B")
    feeding_eating: Optional[Literal["0", "1", "2", "3", "4", "5"]] = Field(None, description="M1870")
    parenteral_iv_feeding_admission: bool = Field(False, description="K0520A1")
    feeding_tube_admission: bool = Field(False, description="K0520B1")
    mechanically_altered_diet_admission: bool = Field(False, description="K0520C1")
    therapeutic_diet_admission: bool = Field(False, description="K0520D1")

class Diagnosis(BaseModel):
    icd10_code: Optional[str] = Field(None, description="ICD-10-CM diagnosis code")
    symptom_control_rating: Optional[Literal["0", "1", "2", "3", "4"]] = Field(None, description="Symptom control rating")

class OASISE1Assessment(BaseModel):
    """
    OASIS-E1 (Outcome and Assessment Information Set Version E1) 
    Home Health Care Assessment Form
    """
    # Core sections
    administrative_info: AdministrativeInfo = Field(default_factory=AdministrativeInfo, description="Section A - Administrative Information")
    sensory_capabilities: SensoryCapabilities = Field(default_factory=SensoryCapabilities, description="Section B - Hearing, Speech, and Vision")
    cognitive_behavioral: CognitiveBehavioralAssessment = Field(default_factory=CognitiveBehavioralAssessment, description="Section C - Cognitive Patterns")
    mood_assessment: MoodAssessment = Field(default_factory=MoodAssessment, description="Section D - Mood")
    functional_status: FunctionalStatus = Field(default_factory=FunctionalStatus, description="Section G - Functional Status")
    self_care: SelfCareAssessment = Field(default_factory=SelfCareAssessment, description="Section GG - Functional Abilities - Self-Care")
    mobility: MobilityAssessment = Field(default_factory=MobilityAssessment, description="Section GG - Functional Abilities - Mobility")
    health_conditions: HealthConditions = Field(default_factory=HealthConditions, description="Section H/J - Health Conditions")
    medications: Medications = Field(default_factory=Medications, description="Section N - Medications")
    skin_conditions: SkinConditions = Field(default_factory=SkinConditions, description="Section M - Skin Conditions")
    nutritional_status: NutritionalStatus = Field(default_factory=NutritionalStatus, description="Section K - Swallowing/Nutritional Status")
    
    # Diagnoses
    primary_diagnosis: Optional[Diagnosis] = Field(None, description="M1021 - Primary Diagnosis")
    other_diagnoses: List[Diagnosis] = Field(default_factory=list, description="M1023 - Other Diagnoses")
    
    # Additional fields
    covid_vaccination_up_to_date: Optional[Literal["0", "1"]] = Field(None, description="O0350")
    influenza_vaccine_received: Optional[Literal["1", "2", "3", "4", "5", "6", "7", "8"]] = Field(None, description="M1046")
    
    class Config:
        use_enum_values = True
        validate_assignment = True
        extra = "forbid"

    @validator('administrative_info')
    def validate_required_admin_fields(cls, v):
        """Ensure critical administrative fields are present"""
        if not v.patient_id and not v.medicare_number and not v.medicaid_number:
            raise ValueError("At least one patient identifier (ID, Medicare, or Medicaid number) is required")
        return v

# Example usage
if __name__ == "__main__":
    # Create a sample assessment
    assessment = OASISE1Assessment(
        administrative_info=AdministrativeInfo(
            patient_id="12345",
            patient_first_name="John",
            patient_last_name="Smith",
            gender=GenderCode.MALE,
            birth_date=date(1945, 3, 15),
            assessment_reason=AssessmentReasonCode.START_OF_CARE,
            assessment_date=date.today()
        ),
        sensory_capabilities=SensoryCapabilities(
            hearing=HearingCode.ADEQUATE,
            vision=VisionCode.IMPAIRED,
            health_literacy="1"
        ),
        functional_status=FunctionalStatus(
            grooming="1",
            bathing="2",
            ambulation="1"
        )
    )
    
    print("OASIS-E1 Assessment Model created successfully!")
    print(f"Patient: {assessment.administrative_info.patient_first_name} {assessment.administrative_info.patient_last_name}")
    print(f"Assessment Date: {assessment.administrative_info.assessment_date}")
    print(f"Assessment JSON: {assessment.json(indent=2)}")