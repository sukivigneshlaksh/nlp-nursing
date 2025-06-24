from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class TemperatureSite(str, Enum):
    oral = "Oral"
    rectal = "Rectal"
    axillary = "Axillary"
    tympanic = "Tympanic"
    temporal = "Temporal"

class PulsePosition(str, Enum):
    sitting = "Sitting"
    standing = "Standing" 
    supine = "Supine"

class PulseSite(str, Enum):
    radial = "Radial"
    brachial = "Brachial"
    carotid = "Carotid"
    femoral = "Femoral"
    apical = "Apical"

class PulseType(str, Enum):
    regular = "Regular"
    irregular = "Irregular"

class VentilatorType(str, Enum):
    spontaneous = "Spontaneous"
    mechanical = "Mechanical"
    bipap = "BiPAP"
    cpap = "CPAP"

class BloodPressurePosition(str, Enum):
    sitting = "Sitting"
    standing = "Standing"
    supine = "Supine"

class BloodPressureSide(str, Enum):
    left = "Left"
    right = "Right"

class OxygenType(str, Enum):
    room_air = "Room Air"
    nasal_cannula = "Nasal Cannula"
    face_mask = "Face Mask"
    non_rebreather = "Non-Rebreather"
    ventilator = "Ventilator"

class OxygenUnit(str, Enum):
    liters = "L/min"
    percent = "%"

class OxygenRoute(str, Enum):
    nasal = "Nasal"
    oral = "Oral"
    tracheostomy = "Tracheostomy"

class MedicalPrognosis(str, Enum):
    good = "Good"
    fair = "Fair"
    poor = "Poor"

class CodeStatus(str, Enum):
    full_code = "Full Code"
    dnr = "DNR"
    dnr_dni = "DNR/DNI"
    comfort_care = "Comfort Care"

class YesNo(str, Enum):
    yes = "Yes"
    no = "No"

class DiabetesType(str, Enum):
    hypoglycemic = "Hypoglycemic"
    hyperglycemic = "Hyperglycemic"
    with_ketoacidosis = "With Ketoacidosis"
    controlled = "Controlled"
    uncontrolled = "Uncontrolled"
    insulin_dependent = "Insulin Dependent"
    type_i = "Type I"
    type_ii = "Type II"

class WoundType(str, Enum):
    pressure = "Pressure"
    surgical = "Surgical"
    deep_tissue_injury = "Deep Tissue Injury"
    partial_thickness = "Partial Thickness"
    full_thickness = "Full Thickness"

class HeartFailureType(str, Enum):
    systolic = "Systolic"
    diastolic = "Diastolic"
    acute = "Acute"
    chronic = "Chronic"
    acute_on_chronic = "Acute on Chronic"

class PrimaryAdmissionCriteria(BaseModel):
    """Primary criteria for LTAC admission"""
    vent_wean: Optional[bool] = Field(None, description="Ventilator weaning")
    respiratory_complex: Optional[bool] = Field(None, description="Respiratory complex care")
    infectious_disease: Optional[bool] = Field(None, description="Infectious disease management")
    wound_skin: Optional[bool] = Field(None, description="Wound/skin care")
    medically_complex: Optional[bool] = Field(None, description="Medically complex")
    cardio_vascular_peripheral: Optional[bool] = Field(None, description="Cardiovascular/peripheral vascular")
    other: Optional[str] = Field(None, description="Other admission criteria")

class ActivelyTreatedComorbidConditions(BaseModel):
    """Comorbid conditions actively being treated"""
    copd_rr_greater_24: Optional[bool] = Field(None, description="COPD and RR > 24")
    alterations_skin_integrity: Optional[bool] = Field(None, description="Alterations in skin integrity requiring complex wound care")
    diabetes_unstable_glucose: Optional[bool] = Field(None, description="Diabetes with unstable glucose")
    chf_symptomatic: Optional[bool] = Field(None, description="CHF: Symptomatic")
    functional_impairment: Optional[bool] = Field(None, description="Functional Impairment")
    respiratory_insufficiency: Optional[bool] = Field(None, description="Respiratory Insufficiency")
    malnutrition: Optional[bool] = Field(None, description="Malnutrition")
    vent_dependent_nippv: Optional[bool] = Field(None, description="Vent Dependent or NIPPV")
    new_onset_infection: Optional[bool] = Field(None, description="New onset symptomatic infection")
    hepatic_insufficiency: Optional[bool] = Field(None, description="Hepatic Insufficiency/Encephalopathy")
    wound: Optional[bool] = Field(None, description="Wound")
    dvt: Optional[bool] = Field(None, description="DVT")
    renal_insufficiency: Optional[bool] = Field(None, description="Renal Insufficiency")
    immunocompromised: Optional[bool] = Field(None, description="Immunocompromised")
    other: Optional[str] = Field(None, description="Other comorbid conditions")

class DiabetesDetails(BaseModel):
    """Detailed diabetes classification"""
    diabetes_types: Optional[List[DiabetesType]] = Field(None, description="Types of diabetes present")

class FunctionalDetails(BaseModel):
    """Functional impairment details"""
    hemiplegia_left: Optional[bool] = Field(None, description="Left hemiplegia/hemiparesis")
    hemiplegia_right: Optional[bool] = Field(None, description="Right hemiplegia/hemiparesis")
    quadriplegia: Optional[bool] = Field(None, description="Quadriplegia/Quadriparesis")
    functional_quadriplegia: Optional[bool] = Field(None, description="Functional Quadriplegia")
    dysphagia: Optional[bool] = Field(None, description="Dysphagia")
    aphasia: Optional[bool] = Field(None, description="Aphasia")

class WoundDetails(BaseModel):
    """Wound assessment details"""
    locations: Optional[List[str]] = Field(None, description="Wound locations")
    wound_types: Optional[List[WoundType]] = Field(None, description="Types of wounds")
    other_wound_details: Optional[str] = Field(None, description="Other wound details")

class CardiacDetails(BaseModel):
    """Cardiac condition details"""
    heart_failure_types: Optional[List[HeartFailureType]] = Field(None, description="Types of heart failure")
    cardiomyopathy: Optional[bool] = Field(None, description="Cardiomyopathy")
    pericarditis: Optional[bool] = Field(None, description="Pericarditis")
    atrial_flutter: Optional[bool] = Field(None, description="Atrial Flutter")
    atrial_fibrillation: Optional[bool] = Field(None, description="Atrial Fibrillation")
    pericardial_effusion: Optional[bool] = Field(None, description="Pericardial Effusion")

class RespiratoryDetails(BaseModel):
    """Respiratory condition details"""
    acute_respiratory_failure: Optional[bool] = Field(None, description="Acute Respiratory Failure")
    chronic_respiratory_failure: Optional[bool] = Field(None, description="Chronic Respiratory Failure")
    pleural_effusion: Optional[bool] = Field(None, description="Pleural Effusion")
    acute_pulmonary_edema: Optional[bool] = Field(None, description="Acute Pulmonary Edema")
    copd: Optional[bool] = Field(None, description="COPD")
    pneumonia: Optional[bool] = Field(None, description="Pneumonia")
    aspiration_pneumonia: Optional[bool] = Field(None, description="Aspiration Pneumonia")
    cpap_bipap: Optional[bool] = Field(None, description="CPAP/BiPAP")
    trach_et_tube: Optional[bool] = Field(None, description="Trach/ET Tube")

class NeurologicalDetails(BaseModel):
    """Neurological condition details"""
    encephalopathy: Optional[bool] = Field(None, description="Encephalopathy")
    acute_metabolic_toxicity: Optional[bool] = Field(None, description="Acute, Metabolic, Toxicity")
    cerebral_edema: Optional[bool] = Field(None, description="Cerebral Edema")
    anoxia: Optional[bool] = Field(None, description="Anoxia")
    coma: Optional[bool] = Field(None, description="Coma")

class GINutritionDetails(BaseModel):
    """GI/Nutrition condition details"""
    severe_malnutrition: Optional[bool] = Field(None, description="Severe Malnutrition")
    cachexia: Optional[bool] = Field(None, description="Cachexia")
    gastroenteritis: Optional[bool] = Field(None, description="Gastroenteritis")
    diverticulitis: Optional[bool] = Field(None, description="Diverticulitis")
    peritonitis: Optional[bool] = Field(None, description="Peritonitis")
    ileus: Optional[bool] = Field(None, description="Ileus")
    post_op: Optional[bool] = Field(None, description="Post-Op")
    acute_pancreatitis: Optional[bool] = Field(None, description="Acute Pancreatitis")
    chronic_pancreatitis: Optional[bool] = Field(None, description="Chronic Pancreatitis")

class InfectionDetails(BaseModel):
    """Infection details"""
    mrsa: Optional[bool] = Field(None, description="MRSA")
    vre: Optional[bool] = Field(None, description="VRE")
    hbv: Optional[bool] = Field(None, description="HBV")
    sepsis: Optional[bool] = Field(None, description="Sepsis")
    osteomyelitis: Optional[bool] = Field(None, description="Osteomyelitis")
    cellulitis: Optional[bool] = Field(None, description="Cellulitis")
    organisms: Optional[List[str]] = Field(None, description="Infectious organisms")
    sites: Optional[List[str]] = Field(None, description="Infection sites")

class ElectrolyteImbalanceDetails(BaseModel):
    """Electrolyte imbalance details"""
    hyponatremia: Optional[bool] = Field(None, description="Hyponatremia")
    hypernatremia: Optional[bool] = Field(None, description="Hypernatremia")
    hypokalemia: Optional[bool] = Field(None, description="Hypokalemia")
    hyperkalemia: Optional[bool] = Field(None, description="Hyperkalemia")

class RenalUrologicDetails(BaseModel):
    """Renal/Urologic condition details"""
    esrd: Optional[bool] = Field(None, description="ESRD")
    uti: Optional[bool] = Field(None, description="UTI")
    ostomy: Optional[bool] = Field(None, description="Ostomy")
    acute_renal_failure: Optional[bool] = Field(None, description="Acute Renal Failure")
    chronic_renal_failure: Optional[bool] = Field(None, description="Chronic Renal Failure")
    chronic_renal_failure_stage: Optional[str] = Field(None, description="Stage of chronic renal failure")

class SurgicalProcedure(BaseModel):
    """Individual surgical procedure"""
    surgery: Optional[str] = Field(None, description="Name of surgical procedure")
    date: Optional[str] = Field(None, description="Date of surgery")
    comments: Optional[str] = Field(None, description="Comments about surgery")

class VitalSigns(BaseModel):
    temperature_f: Optional[float] = Field(None, description="Temperature in Fahrenheit")
    temperature_site: Optional[TemperatureSite] = Field(None, description="Site of temperature measurement")
    temperature_comment: Optional[str] = Field(None, description="Additional temperature comments")
    
    pulse_bpm: Optional[int] = Field(None, description="Pulse rate in beats per minute")
    pulse_position: Optional[PulsePosition] = Field(None, description="Patient position during pulse measurement")
    pulse_site: Optional[PulseSite] = Field(None, description="Site of pulse measurement")
    pulse_type: Optional[PulseType] = Field(None, description="Type/quality of pulse")
    pulse_comment: Optional[str] = Field(None, description="Additional pulse comments")
    
    respirations_per_minute: Optional[int] = Field(None, description="Respiratory rate per minute")
    ventilator_type: Optional[VentilatorType] = Field(None, description="Type of ventilatory support")
    respirations_comment: Optional[str] = Field(None, description="Additional respirations comments")
    
    systolic_bp: Optional[int] = Field(None, description="Systolic blood pressure in mmHg")
    diastolic_bp: Optional[int] = Field(None, description="Diastolic blood pressure in mmHg")
    bp_position: Optional[BloodPressurePosition] = Field(None, description="Patient position during BP measurement")
    bp_side: Optional[BloodPressureSide] = Field(None, description="Arm used for BP measurement")
    bp_comment: Optional[str] = Field(None, description="Additional blood pressure comments")
    
    oxygen_saturation_percent: Optional[int] = Field(None, description="Oxygen saturation percentage")
    oxygen_type: Optional[OxygenType] = Field(None, description="Type of oxygen delivery")
    oxygen_amount: Optional[float] = Field(None, description="Amount of oxygen delivered")
    oxygen_unit: Optional[OxygenUnit] = Field(None, description="Unit of oxygen measurement")
    oxygen_route: Optional[OxygenRoute] = Field(None, description="Route of oxygen delivery")
    oxygen_comment: Optional[str] = Field(None, description="Additional oxygen comments")
    
    blood_glucose_mg_dl: Optional[int] = Field(None, description="Blood glucose in mg/dL")
    glucose_comment: Optional[str] = Field(None, description="Additional glucose comments")

class ReviewOfSystems(BaseModel):
    general: Optional[str] = Field(None, description="General system review")
    neck: Optional[str] = Field(None, description="Neck system review")
    eyes: Optional[str] = Field(None, description="Eyes system review")
    hent: Optional[str] = Field(None, description="Head, Ears, Nose, Throat system review")
    respiratory: Optional[str] = Field(None, description="Respiratory system review")
    cardiovascular: Optional[str] = Field(None, description="Cardiovascular system review")
    gastrointestinal: Optional[str] = Field(None, description="Gastrointestinal system review")
    genitourinary: Optional[str] = Field(None, description="Genitourinary system review")
    musculoskeletal: Optional[str] = Field(None, description="Musculoskeletal system review")
    skin: Optional[str] = Field(None, description="Skin system review")
    endocrine: Optional[str] = Field(None, description="Endocrine system review")
    neurological: Optional[str] = Field(None, description="Neurological system review")
    extremities: Optional[str] = Field(None, description="Extremities system review")
    psychiatric: Optional[str] = Field(None, description="Psychiatric system review")
    hematologic_lymphatic: Optional[str] = Field(None, description="Hematologic/Lymphatic system review")
    other: Optional[str] = Field(None, description="Other system reviews")
    additional_comments: Optional[str] = Field(None, description="Additional review of systems comments")

class PhysicalExamination(BaseModel):
    general: Optional[str] = Field(None, description="General physical examination")
    neck: Optional[str] = Field(None, description="Neck physical examination")
    eyes: Optional[str] = Field(None, description="Eyes physical examination")
    hent: Optional[str] = Field(None, description="Head, Ears, Nose, Throat physical examination")
    respiratory: Optional[str] = Field(None, description="Respiratory physical examination")
    cardiovascular: Optional[str] = Field(None, description="Cardiovascular physical examination")
    gastrointestinal: Optional[str] = Field(None, description="Gastrointestinal physical examination")
    genitourinary: Optional[str] = Field(None, description="Genitourinary physical examination")
    musculoskeletal: Optional[str] = Field(None, description="Musculoskeletal physical examination")
    skin: Optional[str] = Field(None, description="Skin physical examination")
    endocrine: Optional[str] = Field(None, description="Endocrine physical examination")
    neurological: Optional[str] = Field(None, description="Neurological physical examination")
    extremities: Optional[str] = Field(None, description="Extremities physical examination")
    psychiatric: Optional[str] = Field(None, description="Psychiatric physical examination")
    hematologic_lymphatic: Optional[str] = Field(None, description="Hematologic/Lymphatic physical examination")
    other: Optional[str] = Field(None, description="Other physical examination findings")
    additional_comments: Optional[str] = Field(None, description="Additional physical examination comments")

class LabResults(BaseModel):
    """Laboratory results with multiple time points"""
    dates: Optional[List[str]] = Field(None, description="Dates of lab draws")
    sodium: Optional[List[str]] = Field(None, description="Sodium values")
    potassium: Optional[List[str]] = Field(None, description="Potassium values")
    chloride: Optional[List[str]] = Field(None, description="Chloride values")
    co2: Optional[List[str]] = Field(None, description="CO2 values")
    bun: Optional[List[str]] = Field(None, description="BUN values")
    creatinine: Optional[List[str]] = Field(None, description="Creatinine values")
    glucose: Optional[List[str]] = Field(None, description="Glucose values")
    calcium: Optional[List[str]] = Field(None, description="Calcium values")
    phosphorus: Optional[List[str]] = Field(None, description="Phosphorus values")
    magnesium: Optional[List[str]] = Field(None, description="Magnesium values")
    wbc: Optional[List[str]] = Field(None, description="WBC values")
    rbc: Optional[List[str]] = Field(None, description="RBC values")
    hemoglobin: Optional[List[str]] = Field(None, description="Hemoglobin values")
    hematocrit: Optional[List[str]] = Field(None, description="Hematocrit values")
    platelets: Optional[List[str]] = Field(None, description="Platelets values")
    pt_inr: Optional[List[str]] = Field(None, description="PT/INR values")
    ptt: Optional[List[str]] = Field(None, description="PTT values")
    ast: Optional[List[str]] = Field(None, description="AST values")
    alt: Optional[List[str]] = Field(None, description="ALT values")
    alkaline_phosphate: Optional[List[str]] = Field(None, description="Alkaline Phosphate values")
    albumin: Optional[List[str]] = Field(None, description="Albumin values")
    total_protein: Optional[List[str]] = Field(None, description="Total Protein values")
    total_bilirubin: Optional[List[str]] = Field(None, description="Total Bilirubin values")
    crp: Optional[List[str]] = Field(None, description="CRP values")
    esr: Optional[List[str]] = Field(None, description="ESR values")
    tsh: Optional[List[str]] = Field(None, description="TSH values")
    bnp: Optional[List[str]] = Field(None, description="BNP values")
    hba1c: Optional[List[str]] = Field(None, description="HbA1c values")
    ammonia: Optional[List[str]] = Field(None, description="Ammonia values")
    other_labs: Optional[List[str]] = Field(None, description="Other laboratory results")

class Urinalysis(BaseModel):
    """Urinalysis results"""
    date: Optional[str] = Field(None, description="Date of urinalysis")
    specific_gravity: Optional[str] = Field(None, description="Specific gravity")
    ph: Optional[str] = Field(None, description="pH")
    urobilinogen: Optional[str] = Field(None, description="Urobilinogen")
    micro: Optional[str] = Field(None, description="Microscopic examination")
    glucose: Optional[str] = Field(None, description="Glucose")
    ketones: Optional[str] = Field(None, description="Ketones")
    bilirubin: Optional[str] = Field(None, description="Bilirubin")
    blood: Optional[str] = Field(None, description="Blood")
    nitrites: Optional[str] = Field(None, description="Nitrites")
    leukocyte_esterase: Optional[str] = Field(None, description="Leukocyte Esterase")
    protein: Optional[str] = Field(None, description="Protein")
    comments: Optional[str] = Field(None, description="Urinalysis comments")

class ImagingStudy(BaseModel):
    """Individual imaging study"""
    study_type: Optional[str] = Field(None, description="Type of imaging study")
    results_dates_notes: Optional[str] = Field(None, description="Results, dates, and notes")

class PainAssessment(BaseModel):
    """Pain assessment and management"""
    has_pain_complaint: Optional[YesNo] = Field(None, description="Does patient have complaint of pain")
    pain_score: Optional[int] = Field(None, description="Pain score (1-10)")
    pain_description: Optional[str] = Field(None, description="Description of pain")
    pain_management_regimen: Optional[str] = Field(None, description="Pain management regimen")
    pain_management_goals: Optional[str] = Field(None, description="Pain management goals")
    pain_plan_reviewed: Optional[bool] = Field(None, description="Pain assessment and management plan reviewed")

class ScribeAttestation(BaseModel):
    documentation_scribed: Optional[bool] = Field(None, description="Documentation was scribed by individual below")
    scribe_name: Optional[str] = Field(None, description="Name of the scribe")
    practitioner_attestation: Optional[bool] = Field(None, description="Practitioner attests information is accurate")

class VibraLTACHistoryPhysical(BaseModel):
    """Vibra LTAC History & Physical form data"""
    
    # Header Information
    date_of_service: Optional[str] = Field(None, description="Date of service for this H&P")
    late_entry: Optional[bool] = Field(None, description="Indicates if this is a late entry")
    version_date: Optional[str] = Field(None, description="Version date of the form")
    
    # Patient History LTCH
    reason_for_admission: Optional[str] = Field(None, description="Reason for LTAC admission")
    transferring_provider: Optional[str] = Field(None, description="Provider transferring patient")
    consulting_provider: Optional[str] = Field(None, description="Consulting provider")
    chief_complaint: Optional[str] = Field(None, description="Patient's chief complaint")
    history_of_present_illness: Optional[str] = Field(None, description="History of present illness")
    
    # LTAC-specific criteria
    primary_admission_criteria: Optional[PrimaryAdmissionCriteria] = Field(None, description="Primary LTAC admission criteria")
    actively_treated_comorbidities: Optional[ActivelyTreatedComorbidConditions] = Field(None, description="Actively treated comorbid conditions")
    
    # Detailed condition assessments
    diabetes_details: Optional[DiabetesDetails] = Field(None, description="Detailed diabetes assessment")
    functional_details: Optional[FunctionalDetails] = Field(None, description="Functional impairment details")
    wound_details: Optional[WoundDetails] = Field(None, description="Wound assessment details")
    cardiac_details: Optional[CardiacDetails] = Field(None, description="Cardiac condition details")
    respiratory_details: Optional[RespiratoryDetails] = Field(None, description="Respiratory condition details")
    neurological_details: Optional[NeurologicalDetails] = Field(None, description="Neurological condition details")
    gi_nutrition_details: Optional[GINutritionDetails] = Field(None, description="GI/Nutrition condition details")
    infection_details: Optional[InfectionDetails] = Field(None, description="Infection details")
    electrolyte_details: Optional[ElectrolyteImbalanceDetails] = Field(None, description="Electrolyte imbalance details")
    renal_urologic_details: Optional[RenalUrologicDetails] = Field(None, description="Renal/Urologic condition details")
    
    # Surgical history
    surgical_procedures: Optional[List[SurgicalProcedure]] = Field(None, description="Current or past surgical procedures")
    
    # Traditional history sections
    past_medical_history: Optional[str] = Field(None, description="Past medical history")
    past_surgical_history: Optional[str] = Field(None, description="Past surgical history")
    allergies: Optional[str] = Field(None, description="Known allergies")
    medications: Optional[str] = Field(None, description="Current medications")
    diet: Optional[str] = Field(None, description="Dietary requirements")
    code_status: Optional[CodeStatus] = Field(None, description="Code status")
    social_history: Optional[str] = Field(None, description="Social history")
    family_history: Optional[str] = Field(None, description="Family history")
    habits: Optional[str] = Field(None, description="Social habits")
    local_pcp: Optional[str] = Field(None, description="Local primary care physician")
    
    # Review of Systems and Physical Examination
    review_of_systems: Optional[ReviewOfSystems] = Field(None, description="Review of systems")
    vital_signs: Optional[VitalSigns] = Field(None, description="Vital signs")
    physical_examination: Optional[PhysicalExamination] = Field(None, description="Physical examination")
    
    # Laboratory and Diagnostic Studies
    lab_results: Optional[LabResults] = Field(None, description="Laboratory results")
    additional_labs: Optional[str] = Field(None, description="Additional laboratory work")
    urinalysis: Optional[Urinalysis] = Field(None, description="Urinalysis results")
    cultures: Optional[str] = Field(None, description="Culture results")
    imaging_studies: Optional[List[ImagingStudy]] = Field(None, description="Imaging studies")
    procedures_lines: Optional[str] = Field(None, description="Procedures and lines")
    lines_devices: Optional[str] = Field(None, description="Lines and devices")
    
    # Assessment and Plan
    impression_plan: Optional[str] = Field(None, description="Clinical impression and plan")
    medical_prognosis: Optional[MedicalPrognosis] = Field(None, description="Medical prognosis")
    estimated_length_of_stay: Optional[str] = Field(None, description="Estimated length of stay")
    discharge_plan: Optional[str] = Field(None, description="Discharge planning")
    
    # Pain and Admission Criteria
    pain_assessment: Optional[PainAssessment] = Field(None, description="Pain assessment and management")
    admission_criteria_met: Optional[bool] = Field(None, description="LTAC admission criteria met")
    
    # Addendums
    addendum: Optional[str] = Field(None, description="General addendum")
    physician_addendum: Optional[str] = Field(None, description="Physician addendum")
    resident_addendum: Optional[str] = Field(None, description="Resident addendum")
    
    # Scribe Attestation
    scribe_attestation: Optional[ScribeAttestation] = Field(None, description="Scribe attestation information")

# Sample transcript for Vibra LTAC History & Physical
sample_vibra_ltac_hp_transcript = """
VIBRA LTAC HISTORY & PHYSICAL INTERVIEW
Date of Service: June 20, 2025

PHYSICIAN: Good morning, Mr. Davis. I'm Dr. Williams, and I'll be conducting your admission history and physical for the Long Term Acute Care Hospital.

PATIENT: Good morning, Doctor. I've been in the hospital for almost a month now.

PHYSICIAN: You're being transferred from Metro General Hospital for continued complex medical care. Can you tell me what brought you to the hospital originally?
PATIENT: I had pneumonia that got really bad, and then I couldn't breathe on my own. They had to put me on a breathing machine.

PHYSICIAN: You've been on mechanical ventilation for 18 days, and we're going to work on weaning you off the ventilator. That's one of our primary admission criteria - ventilator weaning.
PATIENT: The doctors said this place specializes in getting people off breathing machines.

PHYSICIAN: That's correct. You also have several complex medical conditions we'll be managing. You have COPD with a respiratory rate consistently over 24, which is another criterion for our facility.
PATIENT: Yes, I've had breathing problems for years from smoking.

PHYSICIAN: Your medical history shows you have diabetes that's been difficult to control during this hospitalization, with glucose levels ranging from 180 to 350.
PATIENT: My blood sugar has been all over the place since I got sick.

PHYSICIAN: You also developed a pressure ulcer on your sacrum that requires complex wound care, and you have symptoms of heart failure.
PATIENT: I noticed the sore on my back, and my legs have been swollen.

PHYSICIAN: Do you have any functional impairments? I see in your chart that you have some weakness on your right side.
PATIENT: Yes, I had a small stroke about a year ago. My right arm and leg are weaker than my left.

PHYSICIAN: Your wound is a stage 3 pressure ulcer located on your sacrum. It's a full-thickness wound that will need specialized care.
PATIENT: How long will that take to heal?

PHYSICIAN: With proper treatment, several weeks to months. Now, regarding your heart condition - you have systolic heart failure that's been acute on chronic during this admission.
PATIENT: My heart has been weak for a few years, but it got worse when I got pneumonia.

PHYSICIAN: For your respiratory status, you have acute respiratory failure requiring mechanical ventilation, and chronic respiratory failure from your COPD.
PATIENT: Will I be able to breathe on my own again?

PHYSICIAN: That's our goal. You also developed a pneumonia that we're treating with antibiotics. Your chest X-ray shows improvement.
PATIENT: I hope so. I want to get back home to my family.

PHYSICIAN: Let me review your other medical conditions. You have chronic kidney disease stage 3, and your creatinine has been elevated at 2.1.
PATIENT: My kidneys have been a problem for a while.

PHYSICIAN: You also have some electrolyte imbalances - your sodium has been low at 128, and your potassium was high at 5.2 yesterday.
PATIENT: They keep adjusting my medications because of that.

PHYSICIAN: For your surgical history, you had an appendectomy in 2010 and a cholecystectomy in 2018. Any complications from those?
PATIENT: No, both went fine. No problems.

PHYSICIAN: What allergies do you have?
PATIENT: I'm allergic to penicillin - it gives me hives. And I think I'm allergic to morphine because it makes me very nauseous.

PHYSICIAN: Your current medications include insulin for diabetes, furosemide for heart failure, lisinopril for blood pressure, and antibiotics for the pneumonia.
PATIENT: That sounds right. They give me a lot of shots and pills.

PHYSICIAN: You're on a diabetic, low-sodium diet. Your code status is full code, correct?
PATIENT: Yes, I want everything done if something happens.

PHYSICIAN: Tell me about your social situation. Do you live alone?
PATIENT: I live with my wife in a ranch-style house. She's been so worried about me.

PHYSICIAN: Do you smoke or drink alcohol?
PATIENT: I quit smoking two years ago after 40 years. I used to drink beer on weekends but stopped when I got diabetes.

PHYSICIAN: Your primary care doctor is Dr. Peterson at Family Medicine Associates?
PATIENT: Yes, he's been my doctor for 15 years.

PHYSICIAN: For review of systems, you mentioned shortness of breath. Any chest pain currently?
PATIENT: No chest pain right now, but I get short of breath even with the ventilator sometimes.

PHYSICIAN: Any vision changes or headaches?
PATIENT: No problems with my eyes or headaches.

PHYSICIAN: How about your appetite and bowel movements?
PATIENT: I haven't been eating much because of the breathing tube. My bowel movements have been regular though.

PHYSICIAN: Any urinary problems?
PATIENT: No, the catheter is working fine.

PHYSICIAN: Let me check your vital signs. Temperature is 99.2 degrees Fahrenheit, taken orally.
PATIENT: Is that fever?

PHYSICIAN: It's slightly elevated but not concerning. Your pulse is 95 beats per minute, regular, while you're sitting up in bed.
PATIENT: That feels about normal.

PHYSICIAN: Blood pressure is 150 over 90, taken on your left arm. That's a bit high.
PATIENT: My blood pressure has been high since I got sick.

PHYSICIAN: You're on the ventilator at 16 breaths per minute with some spontaneous breathing.
PATIENT: I've been trying to breathe more on my own.

PHYSICIAN: Oxygen saturation is 96% on 40% oxygen through the ventilator.
PATIENT: Is that good?

PHYSICIAN: That's acceptable. Your blood glucose this morning was 245, which is high.
PATIENT: They're still trying to get my diabetes under control.

PHYSICIAN: For the physical exam, you appear alert and cooperative but with obvious respiratory distress when off the ventilator.
PATIENT: I feel much better when the machine is helping me breathe.

PHYSICIAN: Your lungs have decreased breath sounds at the bases with some crackles. Your heart has a regular rhythm but I can hear a murmur.
PATIENT: Is the murmur new?

PHYSICIAN: It's consistent with your heart failure. Your abdomen is soft but distended, and you have 2+ pitting edema in both legs.
PATIENT: My legs have been swollen for weeks.

PHYSICIAN: Your recent lab work shows a white blood cell count of 12,000, indicating ongoing infection. Your hemoglobin is 8.5, which is low.
PATIENT: Am I anemic?

PHYSICIAN: Yes, likely from your chronic illness. Your kidney function shows a creatinine of 2.1 and BUN of 45.
PATIENT: Are my kidneys getting worse?

PHYSICIAN: We'll monitor them closely. Your chest X-ray shows bilateral infiltrates that are improving, and your echocardiogram shows an ejection fraction of 30%.
PATIENT: What does that mean for my heart?

PHYSICIAN: It confirms significant heart failure, but it's treatable. For your assessment, you have multiple complex conditions requiring long-term acute care.
PATIENT: How long will I need to be here?

PHYSICIAN: I'm estimating 3-4 weeks based on your conditions. My medical prognosis is fair - we'll need special measures to manage your risks.
PATIENT: What are the main risks?

PHYSICIAN: Ventilator-associated complications, heart failure management, infection control, and wound healing.
PATIENT: That sounds serious.

PHYSICIAN: Do you have any pain currently?
PATIENT: Some discomfort from the pressure sore, maybe a 4 out of 10.

PHYSICIAN: We'll work on pain management with both medications and positioning to help healing.
PATIENT: I'd appreciate that.

PHYSICIAN: You definitely meet our admission criteria for long-term acute care, and I agree with the pre-admission assessment.
PATIENT: I'm ready to work hard to get better and go home.

PHYSICIAN: That's exactly the attitude we need. The team will start working with you today on ventilator weaning.
PATIENT: Thank you, Doctor. I'm hopeful about getting off this breathing machine.
"""