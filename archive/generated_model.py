from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from enum import Enum
from dotenv import load_dotenv
import openai
import os

class EducationLevel(str, Enum):
    sixth_grade = "6th grade"
    seventh_grade = "7th grade"
    eighth_grade = "8th grade"
    ninth_grade = "9th grade"
    tenth_grade = "10th grade"
    eleventh_grade = "11th grade"
    high_school_diploma = "High school diploma/GED"
    some_college = "Some college"
    associates_degree = "Associate's degree"
    bachelors_degree = "Bachelor's degree"
    masters_degree = "Master's degree"
    doctoral_degree = "Doctoral degree"

class AlcoholConsumption(str, Enum):
    none = "None"
    light = "Light"
    moderate = "Moderate"
    heavy = "Heavy"

class CaffeineConsumption(str, Enum):
    none = "None"
    light = "Light"
    moderate = "Moderate"
    heavy = "Heavy"

class SmokingStatus(str, Enum):
    never_smoker = "Never smoker"
    former_smoker = "Former smoker"
    current_smoker = "Current smoker"

class PackYears(str, Enum):
    less_than_10 = "Less than 10 Pack Years"
    ten_to_20 = "10-20 Pack Years"
    twenty_to_30 = "20-30 Pack Years"
    thirty_plus = "30+ Pack Years"

class PacksPerDay(str, Enum):
    less_than_half = "Less than 1/2 pack per day"
    half_to_one = "1/2 to 1 pack per day"
    one_to_two = "1-2 packs per day"
    two_to_three = "2-3 packs per day"
    three_or_more = "3 or more packs per day"

class QuitTimeframe(str, Enum):
    less_than_1_year = "Less than 1 year since last cigarette"
    one_to_5_years = "1-5 years since last cigarette"
    five_to_10_years = "5-10 years since last cigarette"
    more_than_10_years = "More than 10 years since last cigarette"

class NicotineFreeStatus(str, Enum):
    never_used = "Never used nicotine-free products"
    formerly_used = "Formerly used nicotine-free products"
    currently_use = "Currently use nicotine-free products"

class PublicHealthTravel(BaseModel):
    recently_traveled_abroad: Optional[bool] = Field(None, description="Have you recently traveled abroad?")
    monkeypox_direct_contact: Optional[bool] = Field(None, description="Have you had direct contact, or contact during intimacy, with monkeypox rash, scabs, or body fluids from a person with monkeypox?")
    monkeypox_object_contact: Optional[bool] = Field(None, description="Have you touched any objects (including fetish gear or sex toys), fabrics (clothing, bedding, or towels), and surfaces that have been used by someone with monkeypox?")
    monkeypox_respiratory_contact: Optional[bool] = Field(None, description="Have you had contact with respiratory secretions from a person with monkeypox?")
    animal_contact_monkeypox: Optional[bool] = Field(None, description="Have you been scratched or bitten by an animal or have you prepared or eaten meat or used products from an animal infected with monkeypox?")
    covid_high_risk_area: Optional[bool] = Field(None, description="Have you been to an area known to be high risk for COVID-19?")
    covid_confirmed_contact: Optional[bool] = Field(None, description="In the 14 days before symptom onset, have you had close contact with a laboratory-confirmed COVID-19 while that case was ill?")
    covid_investigation_contact: Optional[bool] = Field(None, description="In the 14 days before symptom onset, have you had close contact with a person who is under investigation for COVID-19 while that person was ill?")

class EducationOccupation(BaseModel):
    highest_education_level: Optional[EducationLevel] = Field(None, description="What is the highest grade or level of school you have completed or the highest degree you have received?")
    currently_in_school: Optional[bool] = Field(None, description="Are you currently in school?")
    currently_employed: Optional[bool] = Field(None, description="Are you currently employed?")

class ActivitiesDailyLiving(BaseModel):
    able_to_care_for_self: Optional[bool] = Field(None, description="Are you able to care for yourself?")
    blind_or_difficulty_seeing: Optional[bool] = Field(None, description="Are you blind or do you have difficulty seeing?")
    deaf_or_difficulty_hearing: Optional[bool] = Field(None, description="Are you deaf or do you have serious difficulty hearing?")
    difficulty_concentrating: Optional[bool] = Field(None, description="Do you have difficulty concentrating, remembering or making decisions?")
    difficulty_walking: Optional[bool] = Field(None, description="Do you have difficulty walking or climbing stairs?")
    difficulty_dressing_bathing: Optional[bool] = Field(None, description="Do you have difficulty dressing or bathing?")
    difficulty_doing_errands: Optional[bool] = Field(None, description="Do you have difficulty doing errands alone?")

class SubstanceUse(BaseModel):
    tobacco_cessation_counseling_provided: Optional[bool] = Field(None, description="Has tobacco cessation counseling been provided?")
    alcohol_consumption_level: Optional[AlcoholConsumption] = Field(None, description="What is your level of alcohol consumption?")
    uses_illicit_drugs: Optional[bool] = Field(None, description="Do you use any illicit or recreational drugs?")
    illicit_drugs_used: Optional[str] = Field(None, description="Which illicit or recreational drugs have you used?")
    years_using_illicit_drugs: Optional[int] = Field(None, description="How many years have you used illicit or recreational drugs?")
    used_iv_drugs: Optional[bool] = Field(None, description="Have you used IV drugs?")
    illegal_drug_use_past_year: Optional[int] = Field(None, description="How many times in the past year have you used an illegal drug or used a prescription medication for nonmedical reasons?")
    caffeine_consumption_level: Optional[CaffeineConsumption] = Field(None, description="What is your level of caffeine consumption?")
    
    # Tobacco-related fields
    smoking_status: Optional[SmokingStatus] = Field(None, description="Do you or have you ever smoked tobacco?")
    years_smoked_tobacco: Optional[int] = Field(None, description="How many years have you smoked tobacco?")
    age_started_smoking: Optional[int] = Field(None, description="At what age did you start smoking tobacco?")
    current_pack_years: Optional[PackYears] = Field(None, description="What is your current pack years?")
    tobacco_amount_smoked: Optional[PacksPerDay] = Field(None, description="How much tobacco do you smoke?")
    when_quit_smoking: Optional[QuitTimeframe] = Field(None, description="When did you quit smoking?")
    used_nicotine_free_products: Optional[bool] = Field(None, description="Do you or have you ever used any nicotine-free cigarettes, vape, or chewing tobacco?")
    nicotine_free_product_status: Optional[NicotineFreeStatus] = Field(None, description="Do you currently use nicotine-free products or are you a former user of these products?")
    nicotine_free_product_types: Optional[str] = Field(None, description="Which types of nicotine-free products have you used?")
    used_other_tobacco_nicotine: Optional[bool] = Field(None, description="Do you or have you ever used any other forms of tobacco or nicotine?")
    most_recent_tobacco_screening_date: Optional[date] = Field(None, description="What was the date of your most recent tobacco screening?")

class MedicalFormData(BaseModel):
    """Complete medical form data based on the provided form sections"""
    public_health_travel: Optional[PublicHealthTravel] = Field(None, description="Public health and travel related questions")
    education_occupation: Optional[EducationOccupation] = Field(None, description="Education and occupation information")
    activities_daily_living: Optional[ActivitiesDailyLiving] = Field(None, description="Activities of daily living assessment")
    substance_use: Optional[SubstanceUse] = Field(None, description="Substance use history and current status")

client = load_dotenv()

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

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def test_model(MedicalFormData, transcript, bigString):
    response = client.responses.parse(
    model="gpt-4o",
    input=[
        {"role": "system", "content": "Extract medical form data from transcript. Only use explicitly mentioned information."},
        {"role": "user", "content": transcript}
    ],
    text_format=MedicalFormData,
    )
    print(bigString)
    print(response.output_parsed)


# All enums from original
class EducationLevel(str, Enum):
    sixth_grade = "6th grade"
    seventh_grade = "7th grade"
    eighth_grade = "8th grade"
    ninth_grade = "9th grade"
    tenth_grade = "10th grade"
    eleventh_grade = "11th grade"
    high_school_diploma = "High school diploma/GED"
    some_college = "Some college"
    associates_degree = "Associate's degree"
    bachelors_degree = "Bachelor's degree"
    masters_degree = "Master's degree"
    doctoral_degree = "Doctoral degree"

class AlcoholConsumption(str, Enum):
    none = "None"
    light = "Light"
    moderate = "Moderate"
    heavy = "Heavy"

class CaffeineConsumption(str, Enum):
    none = "None"
    light = "Light"
    moderate = "Moderate"
    heavy = "Heavy"

class SmokingStatus(str, Enum):
    never_smoker = "Never smoker"
    former_smoker = "Former smoker"
    current_smoker = "Current smoker"

class PackYears(str, Enum):
    less_than_10 = "Less than 10 Pack Years"
    ten_to_20 = "10-20 Pack Years"
    twenty_to_30 = "20-30 Pack Years"
    thirty_plus = "30+ Pack Years"

class PacksPerDay(str, Enum):
    less_than_half = "Less than 1/2 pack per day"
    half_to_one = "1/2 to 1 pack per day"
    one_to_two = "1-2 packs per day"
    two_to_three = "2-3 packs per day"
    three_or_more = "3 or more packs per day"

class QuitTimeframe(str, Enum):
    less_than_1_year = "Less than 1 year since last cigarette"
    one_to_5_years = "1-5 years since last cigarette"
    five_to_10_years = "5-10 years since last cigarette"
    more_than_10_years = "More than 10 years since last cigarette"

class NicotineFreeStatus(str, Enum):
    never_used = "Never used nicotine-free products"
    formerly_used = "Formerly used nicotine-free products"
    currently_use = "Currently use nicotine-free products"

# All sections from original
class PublicHealthTravel(BaseModel):
    recently_traveled_abroad: Optional[bool] = Field(None, description="Have you recently traveled abroad?")
    monkeypox_direct_contact: Optional[bool] = Field(None, description="Have you had direct contact, or contact during intimacy, with monkeypox rash, scabs, or body fluids from a person with monkeypox?")
    monkeypox_object_contact: Optional[bool] = Field(None, description="Have you touched any objects (including fetish gear or sex toys), fabrics (clothing, bedding, or towels), and surfaces that have been used by someone with monkeypox?")
    monkeypox_respiratory_contact: Optional[bool] = Field(None, description="Have you had contact with respiratory secretions from a person with monkeypox?")
    animal_contact_monkeypox: Optional[bool] = Field(None, description="Have you been scratched or bitten by an animal or have you prepared or eaten meat or used products from an animal infected with monkeypox?")
    covid_high_risk_area: Optional[bool] = Field(None, description="Have you been to an area known to be high risk for COVID-19?")
    covid_confirmed_contact: Optional[bool] = Field(None, description="In the 14 days before symptom onset, have you had close contact with a laboratory-confirmed COVID-19 while that case was ill?")
    covid_investigation_contact: Optional[bool] = Field(None, description="In the 14 days before symptom onset, have you had close contact with a person who is under investigation for COVID-19 while that person was ill?")

class EducationOccupation(BaseModel):
    highest_education_level: Optional[EducationLevel] = Field(None, description="What is the highest grade or level of school you have completed or the highest degree you have received?")
    currently_in_school: Optional[bool] = Field(None, description="Are you currently in school?")
    currently_employed: Optional[bool] = Field(None, description="Are you currently employed?")

class ActivitiesDailyLiving(BaseModel):
    able_to_care_for_self: Optional[bool] = Field(None, description="Are you able to care for yourself?")
    blind_or_difficulty_seeing: Optional[bool] = Field(None, description="Are you blind or do you have difficulty seeing?")
    deaf_or_difficulty_hearing: Optional[bool] = Field(None, description="Are you deaf or do you have serious difficulty hearing?")
    difficulty_concentrating: Optional[bool] = Field(None, description="Do you have difficulty concentrating, remembering or making decisions?")
    difficulty_walking: Optional[bool] = Field(None, description="Do you have difficulty walking or climbing stairs?")
    difficulty_dressing_bathing: Optional[bool] = Field(None, description="Do you have difficulty dressing or bathing?")
    difficulty_doing_errands: Optional[bool] = Field(None, description="Do you have difficulty doing errands alone?")

class SubstanceUse(BaseModel):
    tobacco_cessation_counseling_provided: Optional[bool] = Field(None, description="Has tobacco cessation counseling been provided?")
    alcohol_consumption_level: Optional[AlcoholConsumption] = Field(None, description="What is your level of alcohol consumption?")
    uses_illicit_drugs: Optional[bool] = Field(None, description="Do you use any illicit or recreational drugs?")
    illicit_drugs_used: Optional[str] = Field(None, description="Which illicit or recreational drugs have you used?")
    years_using_illicit_drugs: Optional[int] = Field(None, description="How many years have you used illicit or recreational drugs?")
    used_iv_drugs: Optional[bool] = Field(None, description="Have you used IV drugs?")
    illegal_drug_use_past_year: Optional[int] = Field(None, description="How many times in the past year have you used an illegal drug or used a prescription medication for nonmedical reasons?")
    caffeine_consumption_level: Optional[CaffeineConsumption] = Field(None, description="What is your level of caffeine consumption?")
    smoking_status: Optional[SmokingStatus] = Field(None, description="Do you or have you ever smoked tobacco?")
    years_smoked_tobacco: Optional[int] = Field(None, description="How many years have you smoked tobacco?")
    age_started_smoking: Optional[int] = Field(None, description="At what age did you start smoking tobacco?")
    current_pack_years: Optional[PackYears] = Field(None, description="What is your current pack years?")
    tobacco_amount_smoked: Optional[PacksPerDay] = Field(None, description="How much tobacco do you smoke?")
    when_quit_smoking: Optional[QuitTimeframe] = Field(None, description="When did you quit smoking?")
    used_nicotine_free_products: Optional[bool] = Field(None, description="Do you or have you ever used any nicotine-free cigarettes, vape, or chewing tobacco?")
    nicotine_free_product_status: Optional[NicotineFreeStatus] = Field(None, description="Do you currently use nicotine-free products or are you a former user of these products?")
    nicotine_free_product_types: Optional[str] = Field(None, description="Which types of nicotine-free products have you used?")
    used_other_tobacco_nicotine: Optional[bool] = Field(None, description="Do you or have you ever used any other forms of tobacco or nicotine?")
    most_recent_tobacco_screening_date: Optional[date] = Field(None, description="What was the date of your most recent tobacco screening?")

class FullMedicalFormData(BaseModel):
    public_health_travel: Optional[PublicHealthTravel] = Field(None, description="Public health and travel related questions")
    education_occupation: Optional[EducationOccupation] = Field(None, description="Education and occupation information")
    activities_daily_living: Optional[ActivitiesDailyLiving] = Field(None, description="Activities of daily living assessment")
    substance_use: Optional[SubstanceUse] = Field(None, description="Substance use history and current status")

test_model(FullMedicalFormData, transcript, "Test F: FULL ORIGINAL MODEL")
