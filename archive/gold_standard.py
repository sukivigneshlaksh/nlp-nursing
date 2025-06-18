from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

# Medical Interview Transcript
transcript = """
MEDICAL INTAKE INTERVIEW TRANSCRIPT
Date: June 13, 2025
Patient: Sarah Johnson

NURSE: Good morning, Sarah. I need to go through some standard health screening questions with you today. Let's start with travel and exposure history.

NURSE: Have you recently traveled abroad?
PATIENT: No, I haven't traveled internationally in over two years.

NURSE: Have you had any direct contact with monkeypox - like touching rashes, scabs, or body fluids from someone with monkeypox?
PATIENT: No, absolutely not.

NURSE: Have you touched any objects, fabrics, or surfaces that might have been used by someone with monkeypox?
PATIENT: No, I haven't.

NURSE: Any contact with respiratory secretions from someone with monkeypox?
PATIENT: No.

NURSE: Have you been scratched or bitten by an animal, or eaten meat from an animal that might have been infected with monkeypox?
PATIENT: No, nothing like that.

NURSE: Have you been to any areas considered high risk for COVID-19?
PATIENT: No, I've been staying local.

NURSE: In the past 14 days, have you had close contact with anyone who tested positive for COVID-19?
PATIENT: No, thankfully not.

NURSE: How about contact with anyone under investigation for COVID-19?
PATIENT: No, no contact like that either.

NURSE: Now let's talk about your education and work. What's the highest level of education you've completed?
PATIENT: I have a bachelor's degree. I graduated from Ohio State in 2019.

NURSE: Are you currently in school?
PATIENT: No, I'm not in school anymore.

NURSE: Are you currently employed?
PATIENT: Yes, I work full-time as a marketing coordinator.

NURSE: Let me ask about your daily activities. Are you able to care for yourself - things like bathing, dressing, eating?
PATIENT: Yes, I can take care of myself just fine.

NURSE: Do you have any vision problems - are you blind or have difficulty seeing?
PATIENT: No, my vision is good. I wear contacts but that's it.

NURSE: Any hearing problems - are you deaf or have serious difficulty hearing?
PATIENT: No, my hearing is normal.

NURSE: Do you have difficulty concentrating, remembering things, or making decisions?
PATIENT: No, nothing like that.

NURSE: Do you have trouble walking or climbing stairs?
PATIENT: No, I'm pretty active actually. I go to the gym regularly.

NURSE: Any difficulty dressing or bathing yourself?
PATIENT: No, I can do all that myself.

NURSE: Do you have trouble doing errands alone - like shopping or going to appointments?
PATIENT: No, I do all my errands myself.

NURSE: Now I need to ask about substance use. Has anyone provided you with tobacco cessation counseling?
PATIENT: No, I've never needed that.

NURSE: What's your level of alcohol consumption?
PATIENT: I'd say moderate. I have a glass of wine with dinner maybe 3-4 times a week, sometimes a beer on weekends.

NURSE: Do you use any illicit or recreational drugs?
PATIENT: No, I don't use any illegal drugs.

NURSE: What about caffeine - how much do you consume?
PATIENT: Moderate, I guess. I have my morning coffee and maybe an afternoon tea.

NURSE: Do you smoke tobacco or have you ever smoked?
PATIENT: I used to smoke, but I quit about 3 years ago.

NURSE: How long did you smoke for?
PATIENT: I smoked for about 8 years.

NURSE: What age did you start?
PATIENT: I started when I was 18, in college.

NURSE: At your peak, how much were you smoking?
PATIENT: About half a pack to one pack per day, depending on stress levels.

NURSE: Do you use any nicotine-free products like vaping or chewing tobacco?
PATIENT: No, I've never used any of those.

NURSE: Any other forms of tobacco or nicotine?
PATIENT: No, just cigarettes back when I smoked.

NURSE: When was your last tobacco screening?
PATIENT: That was at my annual physical last month, so May 15th, 2025.
"""

# Extracted Pydantic Model Output
from datetime import date

extracted_data = {
    "public_health_travel": {
        "recently_traveled_abroad": False,
        "monkeypox_direct_contact": False,
        "monkeypox_object_contact": False,
        "monkeypox_respiratory_contact": False,
        "animal_contact_monkeypox": False,
        "covid_high_risk_area": False,
        "covid_confirmed_contact": False,
        "covid_investigation_contact": False
    },
    "education_occupation": {
        "highest_education_level": EducationLevel.bachelors_degree,
        "currently_in_school": False,
        "currently_employed": True
    },
    "activities_daily_living": {
        "able_to_care_for_self": True,
        "blind_or_difficulty_seeing": False,
        "deaf_or_difficulty_hearing": False,
        "difficulty_concentrating": False,
        "difficulty_walking": False,
        "difficulty_dressing_bathing": False,
        "difficulty_doing_errands": False
    },
    "substance_use": {
        "tobacco_cessation_counseling_provided": False,
        "alcohol_consumption_level": AlcoholConsumption.moderate,
        "uses_illicit_drugs": False,
        "illicit_drugs_used": None,
        "years_using_illicit_drugs": None,
        "used_iv_drugs": None,  # Not asked in this interview
        "illegal_drug_use_past_year": None,  # Not asked in this interview
        "caffeine_consumption_level": CaffeineConsumption.moderate,
        "smoking_status": SmokingStatus.former_smoker,
        "years_smoked_tobacco": 8,
        "age_started_smoking": 18,
        "current_pack_years": None,  # Would need calculation
        "tobacco_amount_smoked": PacksPerDay.half_to_one,
        "when_quit_smoking": QuitTimeframe.one_to_5_years,
        "used_nicotine_free_products": False,
        "nicotine_free_product_status": NicotineFreeStatus.never_used,
        "nicotine_free_product_types": None,
        "used_other_tobacco_nicotine": False,
        "most_recent_tobacco_screening_date": date(2025, 5, 15)
    }
}

# Create the Pydantic model instance
medical_form_data = MedicalFormData(**extracted_data)

print("Successfully extracted medical form data:")
print(f"Education Level: {medical_form_data.education_occupation.highest_education_level}")
print(f"Employment Status: {medical_form_data.education_occupation.currently_employed}")
print(f"Smoking Status: {medical_form_data.substance_use.smoking_status}")
print(f"Alcohol Consumption: {medical_form_data.substance_use.alcohol_consumption_level}")
print(f"Last Tobacco Screening: {medical_form_data.substance_use.most_recent_tobacco_screening_date}")

# Validation check
print(f"\nValidation successful! Model created with {len([f for f in medical_form_data.model_fields if getattr(medical_form_data, f) is not None])} populated sections.")

# JSON output
import json
print("\nJSON Output:")
print(json.dumps(medical_form_data.model_dump(), indent=2, default=str))
