
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

class WeightScale(str, Enum):
    bed_scale = "Bed Scale"
    standing_scale = "Standing Scale"
    wheelchair_scale = "Wheelchair Scale"
    lift_scale = "Lift Scale"

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
    
    weight_kg: Optional[float] = Field(None, description="Patient weight in kilograms")
    weight_scale: Optional[WeightScale] = Field(None, description="Type of scale used for weight measurement")
    weight_comment: Optional[str] = Field(None, description="Additional weight comments")

class HistorySection(BaseModel):
    chief_complaint: Optional[str] = Field(None, description="Patient's chief complaint or reason for admission")
    history_of_present_illness: Optional[str] = Field(None, description="Detailed history of current illness or condition")
    past_medical_history: Optional[str] = Field(None, description="Patient's past medical conditions and diagnoses")
    past_surgical_history: Optional[str] = Field(None, description="Patient's previous surgical procedures")
    allergies: Optional[str] = Field(None, description="Known allergies and adverse reactions")
    medications: Optional[str] = Field(None, description="Current medications and dosages")
    diet: Optional[str] = Field(None, description="Dietary restrictions or requirements")
    code_status: Optional[CodeStatus] = Field(None, description="Patient's resuscitation preferences")
    social_functional_history: Optional[str] = Field(None, description="Social history and functional baseline")
    family_history: Optional[str] = Field(None, description="Relevant family medical history")
    family_history_noncontributory: Optional[bool] = Field(None, description="Family history reviewed and noncontributory")

class LabDiagnosticFindings(BaseModel):
    lab_results: Optional[str] = Field(None, description="Laboratory test results")
    diagnostic_findings: Optional[str] = Field(None, description="Diagnostic test findings and imaging results")

class AssessmentPlan(BaseModel):
    assessment_plan: Optional[str] = Field(None, description="Clinical assessment and rehabilitation plan")
    medical_prognosis: Optional[MedicalPrognosis] = Field(None, description="Medical prognosis for rehabilitation stay")
    estimated_length_of_stay: Optional[str] = Field(None, description="Estimated length of rehabilitation stay")
    
    # Pain assessment
    has_pain_complaint: Optional[YesNo] = Field(None, description="Does patient have complaint of pain")
    pain_management_reviewed: Optional[bool] = Field(None, description="Pain assessment and management plan reviewed")
    
    # Admission criteria
    admission_criteria_met: Optional[bool] = Field(None, description="Patient meets IRF admission criteria")
    concurs_with_pas: Optional[bool] = Field(None, description="Physician concurs with PAS assessment")

class ScribeAttestation(BaseModel):
    documentation_scribed: Optional[bool] = Field(None, description="Documentation was scribed by individual below")
    scribe_name: Optional[str] = Field(None, description="Name of the scribe")
    practitioner_attestation: Optional[bool] = Field(None, description="Practitioner attests information is accurate")

class VibraIRFHistoryPhysical(BaseModel):
    """Vibra IRF History & Physical form data"""
    
    # Header Information
    date_of_service: Optional[str] = Field(None, description="Date of service for this H&P")
    late_entry: Optional[bool] = Field(None, description="Indicates if this is a late entry")
    version_date: Optional[str] = Field(None, description="Version date of the form")
    
    # History Section
    history: Optional[HistorySection] = Field(None, description="Comprehensive patient history")
    
    # Review of Systems
    review_of_systems: Optional[str] = Field(None, description="Review of systems findings")
    
    # Physical Examination
    vital_signs: Optional[VitalSigns] = Field(None, description="Patient vital signs and measurements")
    physical_examination: Optional[str] = Field(None, description="Physical examination findings")
    
    # Lab Results and Diagnostic Findings
    lab_diagnostic: Optional[LabDiagnosticFindings] = Field(None, description="Laboratory and diagnostic findings")
    
    # Assessment and Plan
    assessment_plan: Optional[AssessmentPlan] = Field(None, description="Clinical assessment and rehabilitation plan")
    
    # Addendums
    addendum: Optional[str] = Field(None, description="General addendum")
    physician_addendum: Optional[str] = Field(None, description="Physician addendum")
    resident_addendum: Optional[str] = Field(None, description="Resident addendum")
    
    # Scribe Attestation
    scribe_attestation: Optional[ScribeAttestation] = Field(None, description="Scribe attestation information")

# Sample transcript for Vibra IRF History & Physical
sample_vibra_irf_hp_transcript = """
VIBRA IRF HISTORY & PHYSICAL INTERVIEW
Date of Service: June 20, 2025

PHYSICIAN: Good morning, Mrs. Thompson. I'm Dr. Rodriguez, and I'll be conducting your admission history and physical for the rehabilitation hospital.

PATIENT: Good morning, Doctor. I'm ready to start my recovery.

PHYSICIAN: What brings you to our rehabilitation facility today?
PATIENT: I had a stroke three weeks ago and need intensive therapy to get my strength back and learn to walk again.

PHYSICIAN: Can you tell me more about what happened with your stroke?
PATIENT: I was at home making breakfast when suddenly I couldn't move my left arm or leg. My husband called 911 immediately. I was in the regular hospital for two weeks getting treatment.

PHYSICIAN: What medical problems have you had in the past?
PATIENT: I have high blood pressure, diabetes, and high cholesterol. I had a heart attack about five years ago, but I've been doing well since then.

PHYSICIAN: Have you had any surgeries?
PATIENT: Yes, I had my gallbladder removed in 2018 and a knee replacement on my right knee in 2020.

PHYSICIAN: Do you have any allergies to medications?
PATIENT: I'm allergic to penicillin - it gives me a rash.

PHYSICIAN: What medications are you currently taking?
PATIENT: I take metformin for diabetes, lisinopril for blood pressure, atorvastatin for cholesterol, and aspirin. They also started me on a blood thinner after the stroke.

PHYSICIAN: Any dietary restrictions?
PATIENT: I'm on a diabetic diet and they want me to eat low sodium foods.

PHYSICIAN: Have we discussed your code status?
PATIENT: Yes, I want full resuscitation if something happens.

PHYSICIAN: Tell me about your living situation before the stroke.
PATIENT: I live with my husband in a two-story house. I was independent with all my activities. I worked part-time as a librarian and enjoyed gardening.

PHYSICIAN: Any family history of stroke or heart disease?
PATIENT: My father had a stroke when he was 75, and my mother had diabetes. My brother has high blood pressure too.

PHYSICIAN: Let me check your vital signs. Your temperature is 98.2 degrees Fahrenheit, taken orally.
PATIENT: That sounds normal.

PHYSICIAN: Your pulse is 82 beats per minute, regular, taken at your wrist while you're sitting.
PATIENT: Good.

PHYSICIAN: Respirations are 16 per minute, you're breathing on your own without assistance.
PATIENT: Yes, my breathing has been fine.

PHYSICIAN: Blood pressure is 138 over 84, taken on your right arm while sitting.
PATIENT: That's a little high for me, but better than it was in the hospital.

PHYSICIAN: Oxygen saturation is 98% on room air.
PATIENT: I don't need oxygen anymore, which is good.

PHYSICIAN: Your weight today is 72 kilograms on our standing scale.
PATIENT: I think I've lost some weight since this happened.

PHYSICIAN: For the physical exam, you appear alert and oriented. Your speech is clear but you have some weakness on your left side.
PATIENT: Yes, my left arm and leg are much weaker than my right side.

PHYSICIAN: Your recent MRI shows an ischemic stroke in the right middle cerebral artery territory with good recovery potential.
PATIENT: The doctors said I have a good chance of getting better with therapy.

PHYSICIAN: For your assessment, you have a right MCA stroke with left-sided weakness. You're an excellent candidate for intensive rehabilitation. I'm giving you a good prognosis.
PATIENT: How long do you think I'll need to stay here?

PHYSICIAN: Based on your condition and motivation, I estimate about 2-3 weeks of intensive therapy.
PATIENT: That sounds reasonable.

PHYSICIAN: Do you have any pain currently?
PATIENT: No significant pain right now. Maybe some stiffness in my left shoulder, but it's manageable.

PHYSICIAN: We've reviewed pain management strategies with you, including both medication and therapy approaches.
PATIENT: Yes, I understand about managing any pain that comes up.

PHYSICIAN: You definitely meet all criteria for inpatient rehabilitation, and I concur with the pre-admission screening assessment.
PATIENT: I'm ready to work hard to get better.

PHYSICIAN: That's the attitude we like to see. The therapy team will start working with you this afternoon.
PATIENT: I can't wait to begin. I want to go home to my husband and garden again.
"""