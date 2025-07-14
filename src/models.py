from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Medication(BaseModel):
   medication: str
   purpose: str

class Hospitalization(BaseModel):
   hospital: str
   date: Optional[str]
   reason: str

class Surgery(BaseModel):
   surgery: str
   date: Optional[str]

class MedicalHistory(BaseModel):
   name: str
   age: Optional[int]
   date: Optional[str]
   county_of_residence: str
   major_medical_problems: List[str]
   current_doctor: str
   current_medications: List[Medication]
   hospitalizations: List[Hospitalization]
   surgeries: List[Surgery]



class CertificationType(str, Enum):
   INITIAL = "INITIAL"
   RECERTIFICATION = "RECERTIFICATION"

class Sex(str, Enum):
   M = "M"
   F = "F"

class YesNoDoesNotApply(str, Enum):
   Y = "Y"
   N = "N"
   D = "D"

class YesNo(str, Enum):
   Y = "Y"
   N = "N"

class PatientInfo(BaseModel):
   name: str
   address: str
   telephone: str
   hicn: str
   date_of_birth: Optional[str]
   sex: Optional[Sex]
   height_inches: Optional[int]
   weight_lbs: Optional[int]

class SupplierInfo(BaseModel):
   name: str
   address: str
   telephone: str
   nsc_or_npi: str

class PhysicianInfo(BaseModel):
   name: str
   address: str
   nsc_or_npi: str
   telephone: str

class FacilityInfo(BaseModel):
   name: Optional[str]
   address: Optional[str]

class SectionBAnswerer(BaseModel):
   name: Optional[str]
   title: Optional[str]
   employer: Optional[str]

class EquipmentItem(BaseModel):
   description: str
   supplier_charge: Optional[float]
   medicare_fee_schedule_allowance: Optional[float]

class CMSPAPDeviceForm(BaseModel):
   # Section A
   certification_type: CertificationType
   certification_date: Optional[str]
   patient_info: PatientInfo
   supplier_info: SupplierInfo
   physician_info: PhysicianInfo
   place_of_service: str
   facility_info: Optional[FacilityInfo]
   hcpcs_codes: List[str]
   
   # Section B
   estimated_length_of_need_months: Optional[int]  # 1-99, 99=LIFETIME
   diagnosis_codes_icd9: List[str]
   
   # Questions 1-7 (Initial Evaluation)
   q1_obstructive_sleep_apnea: Optional[YesNo]
   q2_initial_face_to_face_date: Optional[str]
   q3_sleep_test_date: Optional[str]
   q4_facility_based_lab: Optional[YesNo]
   q5_ahi_rdi_value: Optional[float]
   q6_documented_evidence_symptoms: Optional[YesNo]
   q7_bilevel_cpap_ineffective: Optional[YesNoDoesNotApply]
   
   # Questions 8-10 (Follow-up Evaluation)
   q8_followup_face_to_face_date: Optional[str]
   q9_pap_usage_compliance: Optional[YesNo]
   q10_symptom_improvement: Optional[YesNo]
   
   section_b_answerer: Optional[SectionBAnswerer]
   
   # Section C
   equipment_items: List[EquipmentItem]
   
   # Section D
   physician_signature_date: Optional[str]

from pydantic import BaseModel
from typing import Optional, List

class TherapyType(str, Enum):
   NEW = "New"
   CONTINUATION = "Continuation of Therapy"

class YesNo(str, Enum):
   YES = "Yes"
   NO = "No"

class AdministrationMethod(str, Enum):
   SELF_ADMINISTERED = "Self-Administered"
   PHYSICIANS_OFFICE = "Physician's Office"
   OTHER = "Other"

class MemberInfo(BaseModel):
   name: str
   member_id: str
   date_of_birth: Optional[str]
   street_address: str
   city: str
   state: str
   zip_code: str
   phone: str
   allergies: str

class PrescriberInfo(BaseModel):
   provider_name: str
   npi: str
   specialty: str
   office_phone: str
   office_fax: str
   office_street_address: str
   city: str
   state: str
   zip_code: str

class MedicationInfo(BaseModel):
   medication: str
   strength: str
   directions_for_use: str
   quantity: str
   administration_method: AdministrationMethod
   administration_other: Optional[str]

class FailedMedication(BaseModel):
   medication: str
   strength: str
   directions: str
   length_of_trial: str
   reason_for_discontinuation: str

class ContraindicatedMedication(BaseModel):
   medication: str
   contraindication_or_intolerance_reason: str

class PriorAuthorizationRequest(BaseModel):
   # Member Information
   member_info: MemberInfo
   
   # Prescriber Information
   prescriber_info: PrescriberInfo
   
   # Therapy Information
   therapy_type: TherapyType
   therapy_start_date: Optional[str]
   currently_hospitalized: YesNo
   recent_discharge_date: Optional[str]
   member_pregnant: YesNo
   due_date: Optional[str]
   
   # Medication Information
   medication_info: MedicationInfo
   
   # Clinical Information
   diagnosis: str
   icd10_codes: List[str]
   failed_medications: List[FailedMedication]
   contraindicated_medications: List[ContraindicatedMedication]
   supporting_lab_results: Optional[str]
   additional_information: Optional[str]
   
   # Provider Signature
   provider_signature_date: Optional[str]

from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class HealthRating(str, Enum):
   EXCELLENT = "Excellent"
   GOOD = "Good"
   FAIR = "Fair"
   POOR = "Poor"

class YesNo(str, Enum):
   YES = "Yes"
   NO = "No"

class FrequencyRating(str, Enum):
   ALWAYS = "Always"
   USUALLY = "Usually"
   SOMETIMES = "Sometimes"
   RARELY = "Rarely"
   NEVER = "Never"

class TwoWeekFrequency(str, Enum):
   NOT_AT_ALL = "Not at all"
   SEVERAL_DAYS = "Several days"
   MORE_THAN_HALF_THE_DAYS = "More than half the days"
   NEARLY_EVERY_DAY = "Nearly every day"

class ExerciseIntensity(str, Enum):
   LIGHT = "Light (like stretching or slow walking)"
   MODERATE = "Moderate (like a brisk walk)"
   HEAVY = "Heavy (like jogging or swimming)"
   VERY_HEAVY = "Very heavy (like fast running or stair climbing)"
   NOT_EXERCISING = "I am currently not exercising"

class FunctionalAbility(str, Enum):
   CAN_DO_MYSELF = "I can do this by myself"
   NEED_SOME_HELP = "I need some help to do it"
   CANNOT_DO = "I cannot do this; another person needs to do it for me"

class YesNoUnsure(str, Enum):
   YES = "Yes"
   NO = "No"
   UNSURE = "Unsure"

class YesNoDontKnow(str, Enum):
   YES = "Yes"
   NO = "No"
   DONT_KNOW = "Don't know / don't remember"

class AdvancePlanningInterest(str, Enum):
   YES = "Yes"
   NO = "No"
   NOT_SURE = "Not sure"

class MobilityAid(str, Enum):
   CANE = "Cane"
   WALKER = "Walker"
   WHEELCHAIR = "Wheelchair"
   CRUTCHES = "Crutches"
   SPECIAL_CHAIR = "Special or built up chair"
   SPECIAL_UTENSILS = "Built up or special utensils"
   DRESSING_DEVICES = "Devices used for dressing (button hook, zipper pull, etc.)"
   NONE = "None of the above"

class PatientInfo(BaseModel):
   name_last: str
   name_first: str
   name_middle_initial: Optional[str]
   birthdate: Optional[str]

class CareProvider(BaseModel):
   name: str
   specialty: Optional[str]

class ScreeningTest(BaseModel):
   where_completed: Optional[str]
   when_completed: Optional[str]
   results_normal: Optional[YesNoUnsure]

class MedicareWellnessAssessment(BaseModel):
   # Basic Information
   todays_date: Optional[str]
   patient_info: PatientInfo
   care_providers_outside_uw: List[CareProvider]
   
   # Self Assessment of Health
   overall_health_rating: Optional[HealthRating]
   can_manage_health_problems: Optional[YesNo]
   need_help_with_personal_care: Optional[YesNo]
   get_emotional_support: Optional[FrequencyRating]
   
   # Psychosocial Health (past 2 weeks)
   feelings_causing_distress: Optional[TwoWeekFrequency]
   feeling_stress: Optional[TwoWeekFrequency]
   body_pain: Optional[TwoWeekFrequency]
   fatigue: Optional[TwoWeekFrequency]
   
   # Health and Habits
   exercise_days_past_week: Optional[int]  # 0-7
   exercise_minutes_per_day: Optional[int]
   exercise_intensity: Optional[ExerciseIntensity]
   fruits_vegetables_frequency: Optional[TwoWeekFrequency]
   high_fiber_foods_frequency: Optional[TwoWeekFrequency]
   mouth_teeth_condition: Optional[HealthRating]
   trouble_hearing: Optional[YesNo]
   wear_hearing_aid: Optional[YesNo]
   always_use_seatbelt: Optional[YesNo]
   have_fire_extinguisher: Optional[YesNo]
   have_smoke_detector: Optional[YesNo]
   
   # Function and Mobility - Activities of Daily Living
   preparing_food_eating: Optional[FunctionalAbility]
   bathing_yourself: Optional[FunctionalAbility]
   getting_dressed: Optional[FunctionalAbility]
   using_toilet: Optional[FunctionalAbility]
   moving_around: Optional[FunctionalAbility]
   
   # Mobility aids used
   mobility_aids: List[MobilityAid]
   
   # Safety and continence
   fallen_or_near_fall_past_year: Optional[YesNo]
   afraid_of_falling: Optional[YesNo]
   balance_issues: Optional[YesNo]
   feel_safe_at_home: Optional[YesNo]
   home_trip_hazards: Optional[YesNo]
   urine_stool_leakage: Optional[YesNo]
   wear_protective_padding: Optional[YesNo]
   
   # Instrumental Activities of Daily Living
   shopping: Optional[FunctionalAbility]
   using_telephone: Optional[FunctionalAbility]
   housekeeping: Optional[FunctionalAbility]
   laundry: Optional[FunctionalAbility]
   driving_transportation: Optional[FunctionalAbility]
   managing_finances: Optional[FunctionalAbility]
   taking_medications: Optional[FunctionalAbility]
   
   # Signs of Memory Issues
   memory_issues_experienced: Optional[YesNo]
   memory_concerns_raised_by_others: Optional[YesNo]
   
   # Screening and Preventive Services
   pneumococcal_vaccines: Optional[ScreeningTest]
   influenza_vaccine: Optional[ScreeningTest]
   hepatitis_b_vaccine: Optional[ScreeningTest]
   mammogram_screening: Optional[ScreeningTest]
   pap_smear: Optional[ScreeningTest]
   colorectal_cancer_screening: Optional[ScreeningTest]
   diabetes_screening: Optional[ScreeningTest]
   cholesterol_panel: Optional[ScreeningTest]
   bone_density_screening: Optional[ScreeningTest]
   eye_exam: Optional[ScreeningTest]
   abdominal_aortic_aneurysm_screening: Optional[ScreeningTest]
   
   # Advanced Care Planning
   has_polst_form: Optional[YesNoDontKnow]
   has_living_will: Optional[YesNoDontKnow]
   has_durable_power_of_attorney: Optional[YesNoDontKnow]
   wants_to_discuss_advance_care_planning: Optional[AdvancePlanningInterest]
   
   # Provider Information
   provider_signature_date: Optional[str]
   provider_name: Optional[str]
   provider_pager: Optional[str]
   provider_npi: Optional[str]
   provider_signature_time: Optional[str]


# OpenAI Structured Output Implementation
from openai import OpenAI
from pydantic import BaseModel
from typing import Union
import os
import base64

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class FormField(BaseModel):
    field_name: str
    label: str
    field_type: str
    value: Optional[str]

class FormSection(BaseModel):
    section_name: str
    fields: List[FormField]

class FilledForm(BaseModel):
    form_name: str
    sections: List[FormSection]
