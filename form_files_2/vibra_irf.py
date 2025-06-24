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

class FunctionalLevel(str, Enum):
    independent = "7 - Complete Independence"
    modified_independent = "6 - Modified Independence"
    supervision = "5 - Supervision"
    minimal_assist = "4 - Minimal Assist"
    moderate_assist = "3 - Moderate Assist"
    maximal_assist = "2 - Maximal Assist"
    total_assist = "1 - Total Assist"

class VitalSigns(BaseModel):
    temperature_f: Optional[float] = Field(None, description="Temperature in Fahrenheit")
    temperature_site: Optional[TemperatureSite] = Field(None, description="Site of temperature measurement")
    temperature_comment: Optional[str] = Field(None, description="Additional temperature comments")
    
    pulse_bpm: Optional[int] = Field(None, description="Pulse rate in beats per minute")
    pulse_position: Optional[PulsePosition] = Field(None, description="Patient position during pulse measurement")
    pulse_site: Optional[PulseSite] = Field(None, description="Site of pulse measurement")
    pulse_type: Optional[PulseType] = Field(None, description="Type/quality of pulse")
    pulse_comment: Optional[str] = Field(None, description="Additional pulse comments")
    
    systolic_bp: Optional[int] = Field(None, description="Systolic blood pressure in mmHg")
    diastolic_bp: Optional[int] = Field(None, description="Diastolic blood pressure in mmHg")
    bp_position: Optional[BloodPressurePosition] = Field(None, description="Patient position during BP measurement")
    bp_side: Optional[BloodPressureSide] = Field(None, description="Arm used for BP measurement")
    bp_comment: Optional[str] = Field(None, description="Additional blood pressure comments")
    
    respirations_per_minute: Optional[int] = Field(None, description="Respiratory rate per minute")
    ventilator_type: Optional[VentilatorType] = Field(None, description="Type of ventilatory support")
    respirations_comment: Optional[str] = Field(None, description="Additional respirations comments")
    
    oxygen_saturation_percent: Optional[int] = Field(None, description="Oxygen saturation percentage")
    oxygen_type: Optional[OxygenType] = Field(None, description="Type of oxygen delivery")
    oxygen_amount: Optional[float] = Field(None, description="Amount of oxygen delivered")
    oxygen_unit: Optional[OxygenUnit] = Field(None, description="Unit of oxygen measurement")
    oxygen_route: Optional[OxygenRoute] = Field(None, description="Route of oxygen delivery")
    oxygen_comment: Optional[str] = Field(None, description="Additional oxygen comments")
    
    weight_kg: Optional[float] = Field(None, description="Patient weight in kilograms")
    weight_scale: Optional[WeightScale] = Field(None, description="Type of scale used for weight measurement")
    weight_comment: Optional[str] = Field(None, description="Additional weight comments")

class FunctionalActivities(BaseModel):
    """Activities of Daily Living functional assessments"""
    
    # Self-care activities
    eating: Optional[str] = Field(None, description="Ability to use suitable utensils to bring food/liquid to mouth and swallow")
    oral_hygiene: Optional[str] = Field(None, description="Ability to use suitable items to clean teeth/dentures")
    toileting_hygiene: Optional[str] = Field(None, description="Ability to adjust clothing before/after void/BM and clean after")
    toilet_transfer: Optional[str] = Field(None, description="Ability to get on and off toilet or bedside commode")
    shower_bathe_self: Optional[str] = Field(None, description="Washing, rinsing, and drying (excludes back and hair)")
    upper_body_dressing: Optional[str] = Field(None, description="Put on/remove shirt, sweater, bra, includes brace/prosthetic")
    lower_body_dressing: Optional[str] = Field(None, description="Put on/remove underwear, pants, skirt, includes brace/prosthetic")
    footwear: Optional[str] = Field(None, description="Putting on/taking off socks and shoes, tying/fastening")
    
    # Mobility activities
    sit_to_lying: Optional[str] = Field(None, description="Move from sitting on side of bed to lying flat")
    lying_to_sitting: Optional[str] = Field(None, description="Move from lying on back to sitting on side of bed")
    sit_to_stand: Optional[str] = Field(None, description="Come to standing position from sitting in chair/wheelchair/bed")
    chair_bed_transfer: Optional[str] = Field(None, description="Move between seated positions on different surfaces")
    walk_10_feet: Optional[str] = Field(None, description="Walk 10 feet in room, corridor, or similar space")
    walk_50_feet_two_turns: Optional[str] = Field(None, description="Walk at least 50 feet and make 2 turns")
    walk_150_feet: Optional[str] = Field(None, description="Walk at least 150 feet in corridor or similar space")
    one_step_curb: Optional[str] = Field(None, description="Go up and down a curb and/or one step")
    four_steps: Optional[str] = Field(None, description="Go up and down four steps with or without rail")

class CurrentFunctionalStatus(BaseModel):
    pt_functional_progress: Optional[str] = Field(None, description="Physical Therapy functional progress notes")
    ot_functional_progress: Optional[str] = Field(None, description="Occupational Therapy functional progress notes")
    st_functional_progress: Optional[str] = Field(None, description="Speech Therapy functional progress notes")
    functional_activities: Optional[FunctionalActivities] = Field(None, description="Detailed functional activity assessments")

class LabDiagnosticFindings(BaseModel):
    lab_results: Optional[str] = Field(None, description="Laboratory test results")
    diagnostic_findings: Optional[str] = Field(None, description="Diagnostic test findings")

class ScribeAttestation(BaseModel):
    documentation_scribed: Optional[bool] = Field(None, description="Documentation was scribed by individual below")
    scribe_name: Optional[str] = Field(None, description="Name of the scribe")
    practitioner_attestation: Optional[bool] = Field(None, description="Practitioner attests information is accurate")

class VibraIRFProgressNote(BaseModel):
    """Vibra IRF (Inpatient Rehabilitation Facility) Progress Note form data"""
    
    # Header Information
    date_of_service: Optional[str] = Field(None, description="Date of service for this progress note")
    late_entry: Optional[bool] = Field(None, description="Indicates if this is a late entry")
    version_date: Optional[str] = Field(None, description="Version date of the form")
    
    # Subjective Section
    subjective: Optional[str] = Field(None, description="Subjective assessment and patient reports")
    review_of_systems: Optional[str] = Field(None, description="Review of systems findings")
    
    # Medications and Vitals
    medications: Optional[str] = Field(None, description="Current medications")
    vital_signs: Optional[VitalSigns] = Field(None, description="Patient vital signs and measurements")
    
    # Physical Examination
    physical_examination: Optional[str] = Field(None, description="Physical examination findings")
    
    # Current Functional Status (IRF-specific)
    current_functional_status: Optional[CurrentFunctionalStatus] = Field(None, description="Rehabilitation functional assessments")
    
    # Lab Results and Diagnostic Findings
    lab_diagnostic: Optional[LabDiagnosticFindings] = Field(None, description="Laboratory and diagnostic findings")
    
    # Assessment and Plan
    assessment_plan: Optional[str] = Field(None, description="Clinical assessment and rehabilitation plan")
    
    # Addendums
    addendum: Optional[str] = Field(None, description="General addendum")
    physician_addendum: Optional[str] = Field(None, description="Physician addendum")
    resident_addendum: Optional[str] = Field(None, description="Resident addendum")
    
    # Scribe Attestation
    scribe_attestation: Optional[ScribeAttestation] = Field(None, description="Scribe attestation information")

# Sample transcript for Vibra IRF Progress Note
sample_vibra_irf_transcript = """
VIBRA IRF PROGRESS NOTE INTERVIEW
Date of Service: June 20, 2025

PHYSICAL THERAPIST: Good morning, Mrs. Anderson. I'm documenting your progress note for today's rehabilitation session.

PATIENT: Good morning. I feel like I'm getting stronger each day.

PHYSICAL THERAPIST: That's great to hear. Let me start with how you're feeling today subjectively.
PATIENT: I feel more confident with my walking. My left leg is still weak but definitely improving. I had some pain in my hip this morning but it's better now.

PHYSICAL THERAPIST: Any issues with your medications or side effects?
PATIENT: No problems with the medications. The pain medication helps without making me too drowsy.

PHYSICAL THERAPIST: Let me check your vital signs. Temperature is 98.4 degrees Fahrenheit, taken orally.
PATIENT: That's normal for me.

PHYSICAL THERAPIST: Pulse is 76 beats per minute, regular, taken at the radial site while you're sitting.
PATIENT: Good, that's in my normal range.

PHYSICAL THERAPIST: Blood pressure is 128 over 82, taken on your right arm while sitting.
PATIENT: That's better than it was when I first came here.

PHYSICAL THERAPIST: Respirations are 18 per minute, breathing on room air.
PATIENT: My breathing has been much easier lately.

PHYSICAL THERAPIST: Oxygen saturation is 97% on room air.
PATIENT: I'm glad I don't need oxygen anymore.

PHYSICAL THERAPIST: Your weight today is 68 kilograms on the standing scale.
PATIENT: I think I've lost a little weight since the surgery.

PHYSICAL THERAPIST: Now let's review your functional progress. For eating, you're now able to use utensils independently.
PATIENT: Yes, I can feed myself completely now. That was one of my biggest goals.

PHYSICAL THERAPIST: For toilet transfers, you're doing this with minimal assistance.
PATIENT: I still need someone nearby for safety, but I can mostly do it myself.

PHYSICAL THERAPIST: Upper body dressing you can do independently now.
PATIENT: That's been much easier. Putting on my shirt and bra is no problem.

PHYSICAL THERAPIST: Lower body dressing still requires moderate assistance.
PATIENT: Yes, getting my pants on is still challenging because of my hip.

PHYSICAL THERAPIST: For mobility, you can now walk 50 feet with two turns using your walker.
PATIENT: I'm proud of that progress. Last week I could barely walk 10 feet.

PHYSICAL THERAPIST: Sit to stand you're doing with supervision only.
PATIENT: I feel much more stable getting up from chairs now.

PHYSICAL THERAPIST: Your recent X-ray shows good healing of the hip fracture.
PATIENT: Dr. Martinez said the bone is healing well.

PHYSICAL THERAPIST: For your assessment and plan, you're making excellent progress with mobility and self-care. We'll continue physical therapy daily and add occupational therapy for advanced ADL training.
PATIENT: How much longer do you think I'll need to stay here?

PHYSICAL THERAPIST: Based on your progress, probably another week or two before you're ready for home with outpatient therapy.
PATIENT: That sounds reasonable. I want to make sure I'm really ready.

PHYSICAL THERAPIST: We'll also have speech therapy evaluate your swallowing since you mentioned some difficulty with liquids yesterday.
PATIENT: Yes, sometimes I feel like liquids go down the wrong way.

OCCUPATIONAL THERAPIST: [Joining the session] Mrs. Anderson is doing well with her occupational therapy goals. She can now shower with supervision and is working on meal preparation skills.
PATIENT: I really want to be able to cook for myself again when I go home.

OCCUPATIONAL THERAPIST: We'll work on that this week. Your fine motor skills are improving daily.
PATIENT: Thank you both for all your help. I feel hopeful about going home.
"""