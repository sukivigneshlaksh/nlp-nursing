"""
Form-Specific Transcripts for Medical Form Processing
====================================================

Comprehensive transcripts tailored to each form type in the system.
Each transcript is designed to provide realistic clinical scenarios
that align with the specific form requirements and fields.

Usage:
    from form_transcripts import FORM_TRANSCRIPTS
    transcript = FORM_TRANSCRIPTS["simple_form"]
"""

# Simple Medical History Form Transcript
SIMPLE_FORM_TRANSCRIPT = """
MEDICAL HISTORY INTAKE INTERVIEW
Date: January 15, 2025
Location: Community Health Center
Provider: Sarah Martinez, RN

NURSE: Good morning! I'm Sarah, and I'll be completing your medical history form today. Let's start with some basic information.

NURSE: What's your full name?
PATIENT: Maria Elena Rodriguez

NURSE: And how old are you, Maria?
PATIENT: I'm 62 years old.

NURSE: What county do you currently live in?
PATIENT: I live in Orange County.

NURSE: Can you tell me about any major medical problems or conditions you have?
PATIENT: Well, I have diabetes - Type 2. I've had it for about 8 years now. I also have high blood pressure, and my doctor says I have high cholesterol. Oh, and I had a small heart attack about three years ago.

NURSE: I'm sorry to hear about that. Who is your current primary care doctor?
PATIENT: Dr. James Wilson at Orange County Family Practice. He's been my doctor for the past five years.

NURSE: What medications are you currently taking?
PATIENT: I take quite a few. There's Metformin for my diabetes - I take that twice a day. For my blood pressure, I take Lisinopril in the morning. I also take Atorvastatin for my cholesterol, and my cardiologist has me on Aspirin and Metoprolol since my heart attack.

NURSE: Have you been hospitalized recently?
PATIENT: Yes, unfortunately. I was at St. Mary's Hospital last September - September 23rd - because my blood sugar got really high and I was dehydrated. Before that, I was hospitalized in March 2022 for my heart attack at Orange County Medical Center.

NURSE: Have you had any surgeries?
PATIENT: I've had a few. Most recently, I had gallbladder surgery in June 2023 - that was June 15th, I remember because it was right before Father's Day. Before that, I had a hysterectomy back in 2018, I think it was in April. And when I was much younger, I had my appendix out - that was way back in 1995.

NURSE: Thank you for all that information, Maria. This will help us provide you with the best care possible.
"""

# CMS PAP Device Form Transcript
CMS_FORM_TRANSCRIPT = """
CMS CERTIFICATE OF MEDICAL NECESSITY - PAP DEVICE
Date: January 15, 2025
Location: Sleep Medicine Associates
Provider: Dr. Michael Chen, MD - Sleep Medicine
Administrative Assistant: Jennifer Kim

ASSISTANT: Good afternoon, Mr. Thompson. I need to complete your CMS Certificate of Medical Necessity for your CPAP machine. This form is required by Medicare to approve coverage.

ASSISTANT: This is an initial certification, correct? You haven't had a CPAP machine before?
PATIENT: That's right, this is my first time needing one.

ASSISTANT: Let me confirm your information. Your full name is Robert James Thompson?
PATIENT: Yes, that's correct.

ASSISTANT: Your address is 456 Oak Street, Sacramento, California 95814?
PATIENT: Yes, that's right.

ASSISTANT: And your phone number is 916-555-0234?
PATIENT: Yes.

ASSISTANT: Your Medicare number is 1EG4-TE5-MK89?
PATIENT: Let me check my card... yes, that looks right.

ASSISTANT: Date of birth March 22, 1958, making you 66 years old?
PATIENT: Correct.

ASSISTANT: You're male, height 6 feet 1 inch, weight 195 pounds?
PATIENT: Yes, though I think I've lost a few pounds recently.

ASSISTANT: Dr. Chen is your sleep medicine physician here at Sleep Medicine Associates, 789 Medical Plaza, Sacramento, CA 95825, phone 916-555-7890. His NPI number is 1234567890.
PATIENT: Yes, Dr. Chen has been great.

ASSISTANT: Your equipment will be supplied by MedEquip Solutions, 321 Supply Avenue, Sacramento, CA 95820, phone 916-555-5555, NPI 9876543210.
PATIENT: That's what Dr. Chen recommended.

ASSISTANT: Now for the clinical questions. Is this device being ordered for treatment of obstructive sleep apnea?
PATIENT: Yes, that's what Dr. Chen diagnosed me with after my sleep study.

ASSISTANT: Your initial face-to-face evaluation with Dr. Chen was on December 10, 2024?
PATIENT: Yes, that was my first appointment after my family doctor referred me.

ASSISTANT: Your sleep study was conducted on January 5, 2025?
PATIENT: Yes, I spent the night at the sleep center here.

ASSISTANT: Was your sleep test conducted in a facility-based lab rather than at home?
PATIENT: Yes, I came here to the sleep center and stayed overnight with all the wires and monitors.

ASSISTANT: Your sleep study showed an AHI - that's Apnea-Hypopnea Index - of 28 events per hour?
PATIENT: Dr. Chen explained that to me. He said 28 was moderate to severe sleep apnea.

ASSISTANT: Do you have documented symptoms like excessive daytime sleepiness, mood disorders, high blood pressure, heart disease, or history of stroke?
PATIENT: Yes, I have high blood pressure, and I'm constantly tired during the day. My wife says I'm more irritable lately, and I sometimes fall asleep watching TV or reading.

ASSISTANT: Since we're prescribing a standard CPAP machine and not a BiPAP, the question about trying CPAP first doesn't apply.
PATIENT: Dr. Chen said we'd start with the CPAP.

ASSISTANT: The equipment being prescribed is a ResMed AirSense 11 CPAP machine with heated humidifier and nasal mask, HCPCS codes E0601 for the machine and E0562 for the humidifier.
PATIENT: That sounds right.

ASSISTANT: The estimated length of need is lifetime, which we code as 99 months for Medicare.
PATIENT: Dr. Chen said this would be permanent.

ASSISTANT: The diagnosis codes are 327.23 for obstructive sleep apnea and 401.9 for essential hypertension.
PATIENT: That matches what Dr. Chen told me.

ASSISTANT: Dr. Chen will review this form and sign it today to certify the medical necessity. Your machine should be delivered within a week.
PATIENT: Perfect, I'm ready to start sleeping better.
"""

# Prior Authorization Form Transcript
PRIOR_AUTH_TRANSCRIPT = """
PRIOR AUTHORIZATION REQUEST CONSULTATION
Date: January 15, 2025
Location: Endocrinology Specialists
Provider: Dr. Patricia Wong, MD - Endocrinologist
Nurse: Lisa Chen, RN

NURSE: Good morning, Mrs. Patterson. Dr. Wong wants to prescribe a new medication for your diabetes, but we need to complete a prior authorization request with your insurance.

NURSE: Let me confirm your information first. Your name is Linda Sue Patterson?
PATIENT: Yes, that's correct.

NURSE: Date of birth is July 8, 1965?
PATIENT: Yes, I'm 59 years old.

NURSE: Your insurance member ID is ABC123456789?
PATIENT: Let me check my card... yes, that's right.

NURSE: Do you have any known drug allergies?
PATIENT: Yes, I'm allergic to penicillin - it gives me a terrible rash. I'm also allergic to sulfa drugs.

NURSE: Are you currently pregnant?
PATIENT: No, definitely not.

NURSE: Are you currently hospitalized?
PATIENT: No, I'm here as an outpatient.

NURSE: Dr. Wong's information - she's at Endocrinology Specialists, 567 Medical Drive, Suite 200, phone 555-123-4567, NPI 2345678901. Her specialty is endocrinology.
PATIENT: Yes, she's been my endocrinologist for two years.

NURSE: This is a new medication request, not a continuation of something you're already taking?
PATIENT: That's right, this would be new for me.

NURSE: The medication Dr. Wong wants to prescribe is Ozempic - that's semaglutide 1mg injection, once weekly subcutaneous injection. You would inject it yourself at home.
PATIENT: She explained that it's a once-a-week shot that should help my diabetes and possibly help me lose some weight.

NURSE: How long would the prescription be for?
PATIENT: Dr. Wong said we'd try it for 90 days initially to see how I respond.

NURSE: Your primary diagnosis is Type 2 diabetes, ICD-10 code E11.9?
PATIENT: Yes, I've had diabetes for about 6 years now.

NURSE: Have you tried other diabetes medications that didn't work well?
PATIENT: Yes, I started with Metformin, but my blood sugar is still too high even on the maximum dose. We tried adding glipizide, but it made me have low blood sugar episodes. Dr. Wong said we need something stronger.

NURSE: Any contraindications or reasons you shouldn't take this medication?
PATIENT: Dr. Wong said I'm a good candidate. No family history of thyroid cancer or anything like that.

NURSE: Have you had recent lab work?
PATIENT: Yes, last week. My A1C was 9.2, which Dr. Wong said is too high. My fasting glucose was 180.

NURSE: We'll submit this request today. Insurance typically responds within 72 hours.
PATIENT: I really hope they approve it. I need to get my diabetes under better control.
"""

# Pain Assessment Care Step Form Transcript
PAIN_ASSESSMENT_TRANSCRIPT = """
PAIN ASSESSMENT NURSING EVALUATION
Date: January 15, 2025
Location: Orthopedic Surgery Unit
Provider: Michael Rodriguez, RN

NURSE: Good morning, Mr. Johnson. I'm Mike, your nurse today. I need to do a comprehensive pain assessment to help us manage your pain better after your surgery.

NURSE: Where is your pain located?
PATIENT: Mainly in my right knee where I had the replacement surgery, but it also goes down into my calf sometimes.

NURSE: Can you describe what area specifically hurts the most?
PATIENT: The whole knee area, but especially on the outer side and the back of my knee. Sometimes it feels like it's deep inside the joint.

NURSE: Tell me about your pain history. How long have you been dealing with knee pain?
PATIENT: Well, I've had arthritis pain for years, but this surgical pain is different. It started right after the surgery three days ago. Before surgery, I had chronic aching for about five years.

NURSE: On a scale of 0 to 10, where 0 is no pain and 10 is the worst pain you can imagine, what number would you give your pain right now?
PATIENT: Right now, I'd say it's about a 6. When I try to move or do physical therapy, it goes up to an 8 or 9.

NURSE: What makes your pain worse?
PATIENT: Movement definitely makes it worse. Trying to bend my knee, walking, even just shifting position in bed. Cold weather used to make my arthritis worse, but now it's mainly movement.

NURSE: What helps relieve your pain?
PATIENT: The pain medication helps some. Ice packs feel good. Keeping my leg elevated and still seems to help too.

NURSE: How would you describe the pain? Is it sharp, dull, burning, throbbing?
PATIENT: It's mostly a deep, throbbing ache that's constant. But when I move, it becomes sharp and stabbing.

NURSE: When did this current pain episode start?
PATIENT: Right after I woke up from surgery on Monday. It's been pretty constant since then.

NURSE: How often does the pain occur?
PATIENT: It's there all the time, but it gets much worse with movement or when the pain medication wears off.

NURSE: How long does each pain episode last?
PATIENT: The constant ache is always there, but the sharp pain when I move lasts for several minutes after I stop moving.

NURSE: Does the pain spread to other areas?
PATIENT: Yes, sometimes it shoots down into my calf, and occasionally I feel it in my hip on the same side.

NURSE: I can see you're guarding your leg and you grimace when you move. Are there other ways you react to the pain?
PATIENT: I try not to move much. I hold my breath when the pain gets bad. Sometimes I clench my fists.

NURSE: Is this pain considered intractable - meaning it's difficult to manage or treat?
PATIENT: The doctors say this is normal post-surgical pain and should improve with time and physical therapy.

NURSE: How are you responding to the current pain treatment?
PATIENT: The pain medication takes the edge off, but it doesn't eliminate the pain completely. The physical therapy is helping, but it's painful during the exercises.

NURSE: Are there any other symptoms that come with your pain?
PATIENT: I feel nauseous sometimes when the pain is really bad. I'm not sleeping well because I can't get comfortable. I feel tired and frustrated.

NURSE: Thank you for all that information. This helps us understand your pain better so we can adjust your treatment plan.
"""

# Wellness Visit Form Transcript
WELLNESS_TRANSCRIPT = """
MEDICARE ANNUAL WELLNESS VISIT
Date: January 15, 2025
Location: Golden Years Family Medicine
Provider: Dr. Sandra Kim, MD - Family Medicine
Nurse: Patricia Thompson, RN

NURSE: Good morning, Mrs. Davis! I'm Patricia, and I'll be helping Dr. Kim with your annual wellness visit today. This is a great benefit that Medicare provides to help keep you healthy.

NURSE: Let me confirm - you're Dorothy Mae Davis, date of birth October 3, 1947, making you 77 years old?
PATIENT: That's right, dear.

NURSE: Do you see any other doctors besides Dr. Kim?
PATIENT: Yes, I see Dr. Martinez, the cardiologist, for my heart. And I see Dr. Patel for my eyes - he's the ophthalmologist. Oh, and I go to Dr. Johnson for my feet sometimes.

NURSE: How would you rate your overall health today? Would you say excellent, very good, good, fair, or poor?
PATIENT: I'd say good. I have my problems, but I'm doing pretty well for my age.

NURSE: How confident are you that you can take good care of your health problems?
PATIENT: Very confident. I've been managing my conditions for years now.

NURSE: Do you feel emotionally distressed, anxious, or depressed?
PATIENT: Sometimes I feel a little down, especially in the winter. But not too bad.

NURSE: How would you rate your stress level - high, moderate, or low?
PATIENT: I'd say low to moderate. My biggest stress is worrying about my husband.

NURSE: Do you have any pain that interferes with your daily activities?
PATIENT: My knees ache sometimes, especially when it's going to rain. But I can still do what I need to do.

NURSE: How would you rate your energy level?
PATIENT: Not as good as it used to be, but fair for my age.

NURSE: Do you exercise regularly?
PATIENT: I try to walk every day, weather permitting. I go to the senior center for water aerobics twice a week.

NURSE: How's your appetite and nutrition?
PATIENT: Pretty good. I try to eat healthy. Sometimes I don't feel like cooking for just me and my husband.

NURSE: Do you wear your seatbelt when driving or riding in a car?
PATIENT: Always. My children drilled that into me years ago.

NURSE: Any problems with your hearing?
PATIENT: I wear hearing aids in both ears. They help a lot.

NURSE: Let's talk about your daily activities. Can you dress yourself, bathe, use the toilet, and eat without help?
PATIENT: Yes, I can do all of that myself.

NURSE: How about managing money, shopping, preparing meals, doing housework, taking medications?
PATIENT: I handle the money and take my medications. My daughter helps with heavy shopping and housework. I can still cook simple meals.

NURSE: Have you fallen in the past year?
PATIENT: I had one small fall last spring in the garden. I wasn't hurt badly, just scraped my hand.

NURSE: Do you ever have problems with urine leakage?
PATIENT: Sometimes, especially when I cough or sneeze. It's not terrible, but it happens.

NURSE: Do you use any walking aids?
PATIENT: I have a cane that I use when I'm walking longer distances or on uneven ground.

NURSE: Any memory concerns?
PATIENT: I forget little things sometimes, but nothing major. I can still remember important things.

NURSE: Let's review your preventive care. When was your last mammogram?
PATIENT: Last year in March. Dr. Kim's office scheduled it.

NURSE: Colonoscopy?
PATIENT: Three years ago. Dr. Martinez said I don't need another one for seven years since everything was normal.

NURSE: Are you up to date on your vaccines - flu shot, pneumonia, shingles?
PATIENT: I get my flu shot every year. I had the pneumonia shot a few years ago. I think I need the shingles vaccine.

NURSE: Do you have advance directives - a living will or power of attorney for healthcare?
PATIENT: Yes, my daughter has my healthcare power of attorney, and I have a living will. We updated them last year.

NURSE: Excellent! Dr. Kim will review everything with you and we'll make sure you're scheduled for any needed screenings or vaccines.
PATIENT: Thank you, dear. You've been very thorough.
"""

# Dictionary of all transcripts for easy access
FORM_TRANSCRIPTS = {
    "simple_form": SIMPLE_FORM_TRANSCRIPT,
    "cms_form": CMS_FORM_TRANSCRIPT,
    "prior_auth_form": PRIOR_AUTH_TRANSCRIPT,
    "pain_assessment": PAIN_ASSESSMENT_TRANSCRIPT,
    "wellness_form": WELLNESS_TRANSCRIPT
}

# Form-specific test cases for the pipeline
FORM_TEST_CASES = [
    {
        "name": "Simple Medical History Form",
        "form_type": "simple_form",
        "pdf_path": "data/pdf/Simple_Form.pdf",
        "transcript": SIMPLE_FORM_TRANSCRIPT,
        "expected_complexity": "simple",
        "key_fields": ["name", "age", "county", "medical problems", "medications"]
    },
    {
        "name": "CMS PAP Device Form",
        "form_type": "cms_form", 
        "pdf_path": "data/pdf/CMS_Form.pdf",
        "transcript": CMS_FORM_TRANSCRIPT,
        "expected_complexity": "moderate",
        "key_fields": ["patient", "physician", "sleep", "cpap"]
    },
    {
        "name": "Prior Authorization Form",
        "form_type": "prior_auth_form",
        "pdf_path": "data/pdf/UHC_form.pdf",
        "transcript": PRIOR_AUTH_TRANSCRIPT,
        "expected_complexity": "moderate", 
        "key_fields": ["member", "prescriber", "medication", "diagnosis"]
    },
    {
        "name": "Pain Assessment Form",
        "form_type": "pain_assessment",
        "pdf_path": "data/pdf/Pain_Assessment_Form.pdf",
        "transcript": PAIN_ASSESSMENT_TRANSCRIPT,
        "expected_complexity": "moderate",
        "key_fields": ["pain", "location", "scale", "medication"]
    },
    {
        "name": "Wellness Visit Form",
        "form_type": "wellness_form",
        "pdf_path": "data/pdf/Wellness_Form.pdf",
        "transcript": WELLNESS_TRANSCRIPT,
        "expected_complexity": "complex",
        "key_fields": ["health", "activities", "memory", "preventive"]
    }
]


def get_transcript_for_form(form_type: str) -> str:
    """Get transcript for specific form type"""
    return FORM_TRANSCRIPTS.get(form_type, "")


def get_test_case_for_form(form_type: str) -> dict:
    """Get test case for specific form type"""
    for test_case in FORM_TEST_CASES:
        if test_case["form_type"] == form_type:
            return test_case
    return {}


def validate_transcript_coverage(form_type: str, transcript: str) -> dict:
    """Validate that transcript covers key fields for form type"""
    test_case = get_test_case_for_form(form_type)
    if not test_case:
        return {"error": f"No test case found for form type: {form_type}"}
    
    key_fields = test_case.get("key_fields", [])
    transcript_lower = transcript.lower()
    
    coverage = {}
    for field in key_fields:
        # Simple keyword matching - could be enhanced with more sophisticated analysis
        field_keywords = field.lower().replace("_", " ").split()
        covered = any(keyword in transcript_lower for keyword in field_keywords)
        coverage[field] = covered
    
    coverage_rate = sum(coverage.values()) / len(coverage) if coverage else 0
    
    return {
        "form_type": form_type,
        "key_fields": key_fields,
        "field_coverage": coverage,
        "coverage_rate": coverage_rate,
        "well_covered": coverage_rate >= 0.7
    }


if __name__ == "__main__":
    # Test transcript coverage for all forms
    print("TRANSCRIPT COVERAGE ANALYSIS")
    print("=" * 40)
    
    for form_type in FORM_TRANSCRIPTS.keys():
        transcript = FORM_TRANSCRIPTS[form_type]
        coverage = validate_transcript_coverage(form_type, transcript)
        
        if 'error' in coverage:
            print(f"\n{form_type.upper()}: {coverage['error']}")
            continue
            
        print(f"\n{form_type.upper()}:")
        print(f"  Coverage Rate: {coverage['coverage_rate']:.1%}")
        print(f"  Well Covered: {'✅' if coverage['well_covered'] else '❌'}")
        
        for field, covered in coverage['field_coverage'].items():
            status = "✅" if covered else "❌"
            print(f"    {field}: {status}")