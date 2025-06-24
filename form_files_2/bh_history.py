from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class YesNoUnknown(str, Enum):
    yes = "Yes"
    no = "No"
    unknown = "Unknown"

class YesNo(str, Enum):
    yes = "Yes"
    no = "No"

class EducationLevel(str, Enum):
    ged = "GED"
    graduated_high_school = "Graduated high school"
    completed_some_high_school = "Completed some high school"
    repeated_grade = "Repeated a grade"
    learning_disability = "Learning disability"
    special_education = "Special education"
    trade_school = "Trade school"
    currently_in_school = "Currently in school"
    completed_some_or_all_college = "Completed some or all of college"
    other = "Other"

class CustodyStatus(str, Enum):
    dcf_custody = "DCF Custody"
    dcf_custody_aftercare = "DCF Custody - Aftercare"
    joint_custody_residential = "Joint Custody (one parent has residential)"
    joint_custody_50_50 = "Joint Custody (50/50)"
    sole_custody = "Sole Custody"
    ppc = "PPC"
    adult_no_guardian = "Adult With No Guardian"
    parental_custody_together = "Parental Custody (parents together)"
    other = "Other"

class LivingArrangement(str, Enum):
    lives_with_spouse = "Lives with spouse"
    lives_with_significant_other = "Lives with significant other"
    lives_with_family = "Lives with family"
    lives_alone = "Lives alone"
    residential_treatment_program = "Residential Treatment Program"
    assisted_living_facility = "Assisted Living Facility"
    skilled_nursing_facility = "Skilled Nursing Facility"
    foster_group_home = "Foster / Group Home"
    homeless = "Homeless"
    has_assistance_in_home = "Has assistance in home"
    other = "Other"

class ExamStatus(str, Enum):
    normal = "Normal"
    abnormal = "Abnormal"
    unable_patient_factors = "Unable to obtain due to patient factors"
    refused_exam = "Refused exam"

class VitalsStatus(str, Enum):
    wnl = "WNL"
    abnormal = "Abnormal"
    unable_patient_factors = "Unable to obtain due to patient factors"
    refused_exam = "Refused exam"

class AbdomenStatus(str, Enum):
    soft_non_tender = "Soft, non-tender, no rebound or rigidity"
    abnormal = "Abnormal"
    unable_patient_factors = "Unable to obtain due to patient factors"
    palpation_nurse_proxy = "Palpation by nurse proxy"
    refused_exam = "Refused exam"

class ENTStatus(str, Enum):
    wnl_typical_landmarks = "WNL With Typical Landmarks"
    abnormal = "Abnormal"
    patient_refused_exam = "Patient Refused Exam"
    unable_patient_factors = "Unable to obtain due to patient factors"
    other = "Other"

class InternalReviewStatus(str, Enum):
    pending = "Pending"
    approved = "Approved"
    needs_revision = "Needs Revision"
    completed = "Completed"

class EducationHistory(BaseModel):
    """Education background information"""
    education_levels: Optional[List[EducationLevel]] = Field(None, description="Educational achievements and challenges")
    other_education: Optional[str] = Field(None, description="Other educational details")

class SocialHistory(BaseModel):
    """Social background and living situation"""
    social_history_details: Optional[str] = Field(None, description="General social history")
    education_history: Optional[EducationHistory] = Field(None, description="Educational background")
    custody_status: Optional[CustodyStatus] = Field(None, description="Current custody arrangement")
    other_custody_status: Optional[str] = Field(None, description="Other custody arrangement details")
    current_living_arrangements: Optional[List[LivingArrangement]] = Field(None, description="Current living situation")
    living_arrangement_other: Optional[str] = Field(None, description="Other living arrangement details")
    facility_name: Optional[str] = Field(None, description="Name of facility if applicable")

class PhysicalExamSection(BaseModel):
    """Individual physical examination section"""
    status: Optional[ExamStatus] = Field(None, description="Examination status")
    details: Optional[str] = Field(None, description="Detailed examination findings")

class VitalsSection(BaseModel):
    """Vital signs examination"""
    status: Optional[VitalsStatus] = Field(None, description="Vital signs status")
    notes: Optional[str] = Field(None, description="Vital signs notes")

class HeadSection(BaseModel):
    """Head examination"""
    atraumatic_normocephalic: Optional[bool] = Field(None, description="Atraumatic, normocephalic")
    status: Optional[ExamStatus] = Field(None, description="Head examination status")
    details: Optional[str] = Field(None, description="Head examination details")

class EyesSection(BaseModel):
    """Eye examination"""
    perrla_eomi_normal: Optional[bool] = Field(None, description="PERRLA, EOMI normal, non-injected conjunctiva")
    status: Optional[ExamStatus] = Field(None, description="Eye examination status")
    details: Optional[str] = Field(None, description="Eye examination details")

class ENTSection(BaseModel):
    """ENT examination"""
    status: Optional[ENTStatus] = Field(None, description="ENT examination status")
    details: Optional[str] = Field(None, description="ENT examination details")

class CardiovascularSection(BaseModel):
    """Cardiovascular examination"""
    regular_rate_rhythm: Optional[bool] = Field(None, description="Regular rate and rhythm without murmur")
    status: Optional[ExamStatus] = Field(None, description="Cardiovascular examination status")
    details: Optional[str] = Field(None, description="Cardiovascular examination details")

class LungsSection(BaseModel):
    """Lung examination"""
    clear_bilaterally: Optional[bool] = Field(None, description="Clear on auscultation, bilaterally")
    status: Optional[ExamStatus] = Field(None, description="Lung examination status")
    details: Optional[str] = Field(None, description="Lung examination details")

class SkinSection(BaseModel):
    """Skin examination"""
    no_rash_wound: Optional[bool] = Field(None, description="No rash or wound observed")
    status: Optional[ExamStatus] = Field(None, description="Skin examination status")
    details: Optional[str] = Field(None, description="Skin examination details")

class AbdomenSection(BaseModel):
    """Abdomen examination"""
    status: Optional[AbdomenStatus] = Field(None, description="Abdomen examination status")
    details: Optional[str] = Field(None, description="Abdomen examination details")

class ExtremitiesSection(BaseModel):
    """Extremities examination"""
    no_clubbing_cyanosis_edema: Optional[bool] = Field(None, description="No clubbing, cyanosis, edema or mass")
    status: Optional[ExamStatus] = Field(None, description="Extremities examination status")
    details: Optional[str] = Field(None, description="Extremities examination details")

class NeurologicalSection(BaseModel):
    """Neurological examination"""
    cn_ii_xii_intact: Optional[bool] = Field(None, description="CN II-XII Grossly Intact")
    status: Optional[ExamStatus] = Field(None, description="Neurological examination status")
    details: Optional[str] = Field(None, description="Neurological examination details")

class PhysicalExamination(BaseModel):
    """Complete physical examination"""
    vitals: Optional[VitalsSection] = Field(None, description="Vital signs")
    head: Optional[HeadSection] = Field(None, description="Head examination")
    eyes: Optional[EyesSection] = Field(None, description="Eye examination")
    ent: Optional[ENTSection] = Field(None, description="ENT examination")
    cardiovascular: Optional[CardiovascularSection] = Field(None, description="Cardiovascular examination")
    lungs: Optional[LungsSection] = Field(None, description="Lung examination")
    skin: Optional[SkinSection] = Field(None, description="Skin examination")
    abdomen: Optional[AbdomenSection] = Field(None, description="Abdomen examination")
    extremities: Optional[ExtremitiesSection] = Field(None, description="Extremities examination")
    neurological: Optional[NeurologicalSection] = Field(None, description="Neurological examination")

class DiagnosesSection(BaseModel):
    """Diagnoses and laboratory findings"""
    labs_diagnostics_reviewed: Optional[YesNo] = Field(None, description="Have labs and diagnostics been reviewed?")
    pertinent_findings_present: Optional[YesNo] = Field(None, description="Any pertinent findings?")
    pertinent_findings_description: Optional[str] = Field(None, description="Description of pertinent findings")
    diagnoses: Optional[str] = Field(None, description="Clinical diagnoses")
    plan_of_care_summary: Optional[str] = Field(None, description="Plan of care summary")

class TimeSpentActivities(BaseModel):
    """Activities included in total service time"""
    reviewing_results_outside_labs: Optional[bool] = Field(None, description="Reviewing Results - Outside Labs/Studies")
    obtaining_reviewing_separate_history: Optional[bool] = Field(None, description="Obtaining/Reviewing Separate History")
    performing_exam_eval: Optional[bool] = Field(None, description="Performing Medically Appropriate Exam/Eval")
    counseling_educating_patient_family: Optional[bool] = Field(None, description="Counseling/Educating Patient/Family")
    ordering_meds_tests_procedures: Optional[bool] = Field(None, description="Ordering Meds, Tests, Procedures")
    referring_communicating_providers: Optional[bool] = Field(None, description="Referring/Communicating with other Providers")
    documenting_clinical_info_ehr: Optional[bool] = Field(None, description="Documenting clinical info in the EHR")
    care_coordination: Optional[bool] = Field(None, description="Care Coordination")
    other_activities: Optional[str] = Field(None, description="Other activities")

class ServiceDetails(BaseModel):
    """Service delivery details"""
    was_telehealth_service: Optional[YesNo] = Field(None, description="Was this a Tele-Health Service?")
    time_spent_activities: Optional[TimeSpentActivities] = Field(None, description="Activities included in total time")
    date_of_service: Optional[str] = Field(None, description="Date of service")
    duration_minutes: Optional[int] = Field(None, description="Duration in minutes")

class InternalReview(BaseModel):
    """Internal quality review"""
    date_of_review: Optional[str] = Field(None, description="Date of internal review")
    reviewed_by: Optional[str] = Field(None, description="Reviewer name/ID")
    internal_review_status: Optional[InternalReviewStatus] = Field(None, description="Review status")

class GeneralHistoryPhysical(BaseModel):
    """General History and Physical Examination form data"""
    
    # Header Information
    version_date: Optional[str] = Field(None, description="Version date of the form")
    
    # History Section
    chief_complaint: Optional[str] = Field(None, description="Patient's chief complaint")
    history_of_present_illness: Optional[str] = Field(None, description="History of present illness")
    
    # Medical Conditions
    past_present_medical_conditions: Optional[YesNoUnknown] = Field(None, description="Past or present medical conditions")
    medical_conditions_description: Optional[str] = Field(None, description="Description of medical conditions, onset, treatment, devices")
    
    # Social History
    social_history: Optional[SocialHistory] = Field(None, description="Social background and living situation")
    
    # Medications and Allergies
    allergies: Optional[str] = Field(None, description="Known allergies")
    current_medications: Optional[str] = Field(None, description="Current medications")
    
    # Physical Examination
    physical_examination: Optional[PhysicalExamination] = Field(None, description="Complete physical examination")
    
    # Diagnoses and Plan
    diagnoses: Optional[DiagnosesSection] = Field(None, description="Diagnoses and laboratory findings")
    
    # Service Details
    service_details: Optional[ServiceDetails] = Field(None, description="Service delivery details")
    
    # Internal Review
    internal_review: Optional[InternalReview] = Field(None, description="Internal quality review")

# Sample transcript for General History & Physical
sample_general_hp_transcript = """
GENERAL HISTORY & PHYSICAL EXAMINATION
Date: June 20, 2025

PHYSICIAN: Good afternoon, Alex. I'm Dr. Martinez, and I'll be doing your history and physical exam today.

PATIENT: Hi, Dr. Martinez. Thanks for seeing me.

PHYSICIAN: What brings you in today? What's your main concern?
PATIENT: I've been having stomach pain for about three days, and it's gotten worse since yesterday.

PHYSICIAN: Can you tell me more about when this stomach pain started and what it feels like?
PATIENT: It started Sunday after dinner. It's a sharp pain in my lower right side that gets worse when I move or cough.

PHYSICIAN: Have you had any medical problems in the past or are you dealing with any ongoing health issues?
PATIENT: I had my appendix out when I was 12, and I have asthma. I use an inhaler when I need it.

PHYSICIAN: Let me ask about your social situation. What's your educational background?
PATIENT: I graduated from high school last year, and I'm currently taking some college classes part-time.

PHYSICIAN: What's your living situation and custody arrangement?
PATIENT: I live with my parents. They're still together, so it's just regular parental custody.

PHYSICIAN: Where are you living currently?
PATIENT: I live with my family in our house. We don't need any special assistance or anything.

PHYSICIAN: Do you have any known allergies to medications?
PATIENT: I'm allergic to penicillin - it gives me a bad rash.

PHYSICIAN: What medications are you currently taking?
PATIENT: Just my albuterol inhaler for asthma, and I take ibuprofen sometimes for headaches.

PHYSICIAN: Now let me do your physical examination. Your vital signs look normal - temperature, blood pressure, and pulse are all within normal limits.
PATIENT: That's good to hear.

PHYSICIAN: Your head appears normal - atraumatic and normocephalic, no bumps or injuries.
PATIENT: Yeah, I haven't hit my head or anything.

PHYSICIAN: Your eyes look good - pupils are equal, round, and reactive to light, and your eye movements are normal.
PATIENT: My vision has been fine.

PHYSICIAN: Your ears, nose, and throat all look normal with typical landmarks.
PATIENT: I haven't had any ear or throat problems.

PHYSICIAN: Your heart has a regular rate and rhythm, and I don't hear any murmurs.
PATIENT: Good, I was worried about my heart racing earlier.

PHYSICIAN: Your lungs are clear on both sides when I listen.
PATIENT: My breathing has been okay, no asthma problems lately.

PHYSICIAN: I don't see any rash or wounds on your skin.
PATIENT: Right, just the stomach pain is bothering me.

PHYSICIAN: Now for your abdomen - I can feel that it's tender in the lower right area, and there's some guarding when I press.
PATIENT: Ow, yes, that's exactly where it hurts the most.

PHYSICIAN: Your arms and legs look normal - no swelling, discoloration, or masses.
PATIENT: Yeah, everything else feels fine.

PHYSICIAN: Your neurological exam is normal - all your cranial nerves are working properly.
PATIENT: I haven't had any numbness or weakness.

PHYSICIAN: Have you had any lab work or imaging done for this?
PATIENT: No, this is my first visit for this problem.

PHYSICIAN: Based on your symptoms and physical exam, I'm concerned about possible appendicitis, even though you had your appendix removed before.
PATIENT: Can that happen again?

PHYSICIAN: Sometimes there can be incomplete removal or other causes of similar pain. I want to get some blood work and a CT scan to be safe.
PATIENT: Okay, whatever you think is best.

PHYSICIAN: My plan is to get labs including a complete blood count and inflammatory markers, and a CT scan of your abdomen and pelvis.
PATIENT: How long will that take?

PHYSICIAN: The labs will be back in about an hour, and the CT scan should be done within two hours.
PATIENT: Will I need surgery?

PHYSICIAN: Let's see what the tests show first. We'll take good care of you and make sure we figure out what's causing your pain.
PATIENT: Thank you, Dr. Martinez. I appreciate you taking this seriously.

ADMINISTRATIVE STAFF: Dr. Martinez, was this visit conducted via telehealth?
PHYSICIAN: No, this was an in-person examination in the clinic.

ADMINISTRATIVE STAFF: Can you detail the time spent on this visit?
PHYSICIAN: I spent time obtaining a detailed history, performing a comprehensive physical examination, counseling the patient about the findings, and ordering appropriate tests. Total time was approximately 35 minutes.

ADMINISTRATIVE STAFF: This case will be reviewed as part of our quality assurance process.
PHYSICIAN: Please have Dr. Johnson review this case, especially given the history of prior appendectomy.
"""