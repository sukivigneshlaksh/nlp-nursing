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

class LabDiagnosticFindings(BaseModel):
    lab_results: Optional[str] = Field(None, description="Laboratory test results")
    diagnostic_findings: Optional[str] = Field(None, description="Diagnostic test findings")

class ScribeAttestation(BaseModel):
    documentation_scribed: Optional[bool] = Field(None, description="Documentation was scribed by individual below")
    scribe_name: Optional[str] = Field(None, description="Name of the scribe")
    practitioner_attestation: Optional[bool] = Field(None, description="Practitioner attests information is accurate")

class VibraLTACProgressNote(BaseModel):
    """Vibra LTAC Provider Progress Note form data"""
    
    # Header Information
    date: Optional[str] = Field(None, description="Date of the progress note")
    version_date: Optional[str] = Field(None, description="Version date of the form")
    
    # Subjective Section
    subjective: Optional[str] = Field(None, description="Subjective assessment and patient complaints")
    
    # Objective Section
    objective: Optional[str] = Field(None, description="Objective findings and observations")
    medications: Optional[str] = Field(None, description="Current medications")
    vital_signs: Optional[VitalSigns] = Field(None, description="Patient vital signs")
    
    # Review of Systems
    review_of_systems: Optional[ReviewOfSystems] = Field(None, description="Review of systems findings")
    
    # Physical Examination
    physical_examination: Optional[PhysicalExamination] = Field(None, description="Physical examination findings")
    
    # Lab Results and Diagnostic Findings
    lab_diagnostic: Optional[LabDiagnosticFindings] = Field(None, description="Laboratory and diagnostic findings")
    
    # Assessment and Plan
    assessment_plan: Optional[str] = Field(None, description="Clinical assessment and treatment plan")
    
    # Addendums
    addendum: Optional[str] = Field(None, description="General addendum")
    physician_addendum: Optional[str] = Field(None, description="Physician addendum")
    resident_addendum: Optional[str] = Field(None, description="Resident addendum")
    
    # Scribe Attestation
    scribe_attestation: Optional[ScribeAttestation] = Field(None, description="Scribe attestation information")

# Sample transcript for Vibra LTAC Progress Note
sample_vibra_ltac_transcript = """
VIBRA LTAC PROVIDER PROGRESS NOTE INTERVIEW
Date: June 20, 2025

NURSE: I'm completing today's progress note for Mr. Johnson. Let me gather the information.

NURSE: How are you feeling today, Mr. Johnson?
PATIENT: I'm feeling a bit better than yesterday. Still having some shortness of breath but not as bad.

NURSE: Any chest pain or discomfort?
PATIENT: No chest pain today, just the breathing issue.

NURSE: Let me check your vital signs. Temperature is 98.6 degrees Fahrenheit, taken orally.
PATIENT: Okay.

NURSE: Your pulse is 88 beats per minute, regular, taken at the radial site while you're sitting.
PATIENT: That sounds normal.

NURSE: Respirations are 22 per minute, you're on BiPAP support overnight.
PATIENT: Yes, the BiPAP helps me sleep better.

NURSE: Blood pressure is 142 over 88, taken on your left arm while sitting.
PATIENT: That's a bit high for me.

NURSE: Oxygen saturation is 94% on 2 liters per minute via nasal cannula.
PATIENT: I've been on oxygen for a few days now.

NURSE: Blood glucose this morning was 156 mg/dL.
PATIENT: That's higher than usual, probably from the medications.

NURSE: For review of systems - any fever, chills, or night sweats?
PATIENT: No fever or chills, but I did have some night sweats.

NURSE: Any vision changes or eye problems?
PATIENT: No, vision is fine.

NURSE: How about your breathing - any cough or sputum production?
PATIENT: Yes, I have a productive cough with yellow sputum.

NURSE: Any chest pain or palpitations?
PATIENT: No chest pain, but I sometimes feel my heart racing.

NURSE: Bowel movements regular? Any nausea or vomiting?
PATIENT: Bowel movements are normal, no nausea.

NURSE: Any urinary problems or changes?
PATIENT: No problems with urination.

NURSE: Now for the physical exam. You appear comfortable but mildly short of breath.
PATIENT: I feel okay when I'm sitting up.

NURSE: Lungs have some crackles at the bases bilaterally.
PATIENT: That's what the doctor mentioned yesterday.

NURSE: Heart rate is regular, no murmurs heard.
PATIENT: Good to hear.

NURSE: Abdomen is soft, non-tender, bowel sounds present.
PATIENT: No stomach pain.

NURSE: Your recent chest X-ray shows bilateral lower lobe infiltrates.
PATIENT: Is that pneumonia?

NURSE: Dr. Smith will discuss the results with you, but you're being treated with antibiotics.
PATIENT: I've been taking the IV antibiotics.

NURSE: For the assessment and plan - you have pneumonia that's improving with antibiotic therapy. We'll continue the current treatment.
PATIENT: How much longer will I need to stay?

NURSE: Dr. Smith will make that determination based on your progress over the next few days.
PATIENT: I hope I can go home soon.
"""