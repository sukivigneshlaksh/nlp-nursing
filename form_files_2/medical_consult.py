from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class YesNo(str, Enum):
    yes = "Yes"
    no = "No"

class InternalReviewStatus(str, Enum):
    pending = "Pending"
    approved = "Approved"
    needs_revision = "Needs Revision"
    completed = "Completed"

class TimeSpentActivities(BaseModel):
    """Activities included in total consultation time"""
    reviewing_results_outside_labs: Optional[bool] = Field(None, description="Reviewing Results - Outside Labs/Studies")
    obtaining_reviewing_separate_history: Optional[bool] = Field(None, description="Obtaining/Reviewing Separate History")
    performing_exam_eval: Optional[bool] = Field(None, description="Performing Medically Appropriate Exam/Eval")
    counseling_educating_patient_family: Optional[bool] = Field(None, description="Counseling/Educating Patient/Family")
    ordering_meds_tests_procedures: Optional[bool] = Field(None, description="Ordering Meds, Tests, Procedures")
    referring_communicating_providers: Optional[bool] = Field(None, description="Referring/Communicating with other Providers")
    documenting_clinical_info_ehr: Optional[bool] = Field(None, description="Documenting clinical info in the EHR")
    care_coordination: Optional[bool] = Field(None, description="Care Coordination")
    other_activities: Optional[str] = Field(None, description="Other activities performed during consultation")

class ServiceDetails(BaseModel):
    """Service delivery and billing details"""
    was_telehealth_service: Optional[YesNo] = Field(None, description="Was this a Tele-Health Service?")
    time_spent_activities: Optional[TimeSpentActivities] = Field(None, description="Activities included in total time")
    date_of_service: Optional[str] = Field(None, description="Date consultation was performed")
    duration_minutes: Optional[int] = Field(None, description="Total duration of consultation in minutes")

class InternalReview(BaseModel):
    """Internal quality review information"""
    date_of_review: Optional[str] = Field(None, description="Date of internal review")
    reviewed_by: Optional[str] = Field(None, description="Name/ID of reviewer")
    internal_review_status: Optional[InternalReviewStatus] = Field(None, description="Status of internal review")

class MedicalConsult(BaseModel):
    """Medical Consult form data"""
    
    # Header Information
    version_date: Optional[str] = Field(None, description="Version date of the form")
    
    # Medical Consult Section
    reason_for_consultation: Optional[str] = Field(None, description="Reason why consultation was requested")
    findings_and_history: Optional[str] = Field(None, description="Clinical findings and history of present illness")
    diagnosis: Optional[str] = Field(None, description="Consultant's diagnosis or clinical impression")
    recommendations_and_plan: Optional[str] = Field(None, description="Treatment recommendations and plan")
    
    # Service Details
    service_details: Optional[ServiceDetails] = Field(None, description="Service delivery and billing information")
    
    # Internal Review
    internal_review: Optional[InternalReview] = Field(None, description="Internal quality review information")

# Sample transcript for Medical Consult
sample_medical_consult_transcript = """
MEDICAL CONSULTATION DOCUMENTATION
Date: June 20, 2025

CONSULTING PHYSICIAN: This is Dr. Sarah Chen, Cardiology, providing consultation on patient Maria Rodriguez.

CONSULTING PHYSICIAN: I was asked to see this patient for evaluation of chest pain and abnormal EKG findings.
PATIENT: I've been having chest tightness for the past three days, especially when I walk upstairs.

CONSULTING PHYSICIAN: Can you describe the chest pain in more detail?
PATIENT: It feels like pressure in the center of my chest. It goes away when I rest for a few minutes.

CONSULTING PHYSICIAN: Any radiation of the pain to your arms, neck, or jaw?
PATIENT: Sometimes I feel it in my left arm, but not always.

CONSULTING PHYSICIAN: The patient was referred from the emergency department after presenting with chest pain. Her EKG showed some ST depression in leads V4-V6. Her troponin levels were slightly elevated at 0.08.
PATIENT: The ER doctor said my heart test was a little abnormal.

CONSULTING PHYSICIAN: I've reviewed her outside lab results from this morning. The troponin has increased to 0.12, which is concerning.
PATIENT: Is that bad?

CONSULTING PHYSICIAN: On examination, the patient appears comfortable at rest. Heart rate is regular at 78 beats per minute. Blood pressure is 145/90. Heart sounds are normal with no murmurs. Lungs are clear.
PATIENT: I do feel better when I'm sitting still.

CONSULTING PHYSICIAN: Based on the clinical presentation, elevated troponins, and EKG changes, my diagnosis is non-ST elevation myocardial infarction, also known as NSTEMI.
PATIENT: Does that mean I had a heart attack?

CONSULTING PHYSICIAN: Yes, it's a type of heart attack. The good news is we caught it early and can treat it effectively.
PATIENT: What happens now?

CONSULTING PHYSICIAN: My recommendations are to start dual antiplatelet therapy with aspirin and clopidogrel, initiate atorvastatin for cholesterol management, and begin metoprolol for blood pressure control. I'm also ordering a cardiac catheterization for tomorrow morning.
PATIENT: Will I need surgery?

CONSULTING PHYSICIAN: The catheterization will show us if you need a stent or other intervention. I'm also referring you to our cardiac rehabilitation program for after discharge.
PATIENT: How long will I be in the hospital?

CONSULTING PHYSICIAN: Typically 2-3 days, depending on the catheterization results and how you respond to treatment.
PATIENT: I'm scared, but I'm glad you caught this.

CONSULTING PHYSICIAN: You're in good hands. The nursing staff will monitor you closely tonight, and I'll check on you before the procedure tomorrow.

ADMINISTRATIVE STAFF: Dr. Chen, was this consultation conducted via telehealth?
CONSULTING PHYSICIAN: No, this was an in-person consultation in the cardiac care unit.

ADMINISTRATIVE STAFF: Can you detail the time spent on this consultation?
CONSULTING PHYSICIAN: I spent time reviewing her outside lab results and EKG, obtaining additional history about her symptoms, performing a focused cardiac examination, counseling her and her family about the diagnosis, ordering medications and the cardiac catheterization procedure, and coordinating care with the interventional cardiology team. Total time was approximately 45 minutes.

ADMINISTRATIVE STAFF: The consultation has been submitted for internal review.
CONSULTING PHYSICIAN: Please have Dr. Martinez review this case as part of our quality assurance process.

PATIENT: Thank you for explaining everything so clearly, Dr. Chen.
CONSULTING PHYSICIAN: You're welcome. The nurses have my contact information if you have any questions tonight.
"""