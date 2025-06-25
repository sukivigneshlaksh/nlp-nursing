from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class HealthRating(str, Enum):
    excellent = "Excellent"
    good = "Good"
    fair = "Fair"
    poor = "Poor"

class YesNo(str, Enum):
    yes = "Yes"
    no = "No"

class EmotionalSupport(str, Enum):
    always = "Always"
    usually = "Usually"
    sometimes = "Sometimes"
    rarely = "Rarely"
    never = "Never"

class Frequency(str, Enum):
    not_at_all = "Not at all"
    several_days = "Several days"
    more_than_half_days = "More than half the days"
    nearly_every_day = "Nearly every day"

class ExerciseIntensity(str, Enum):
    light = "Light (like stretching or slow walking)"
    moderate = "Moderate (like a brisk walk)"
    heavy = "Heavy (like jogging or swimming)"
    very_heavy = "Very heavy (like fast running or stair climbing)"
    not_exercising = "I am currently not exercising"

class AbilityLevel(str, Enum):
    can_do_myself = "I can do this by myself"
    need_some_help = "I need some help to do it"
    cannot_do = "I cannot do this; another person needs to do it for me"

class DontKnow(str, Enum):
    yes = "Yes"
    no = "No"
    dont_know = "Don't know / don't remember"

class NormalResults(str, Enum):
    yes = "Yes"
    no = "No"
    unsure = "Unsure"

class BasicInfo(BaseModel):
    name: Optional[str] = Field(None, description="Patient's full name")
    birthdate: Optional[str] = Field(None, description="Patient's date of birth")
    todays_date: Optional[str] = Field(None, description="Date of the wellness visit")

class CareProviders(BaseModel):
    outside_providers: Optional[List[str]] = Field(None, description="List of care providers outside UW Medicine")

class SelfAssessment(BaseModel):
    overall_health_rating: Optional[HealthRating] = Field(None, description="How patient rates overall health in past 4 weeks")
    can_manage_health_problems: Optional[YesNo] = Field(None, description="Can patient manage overall health problems")
    needs_help_personal_care: Optional[YesNo] = Field(None, description="Does patient need help with personal care needs")
    emotional_support: Optional[EmotionalSupport] = Field(None, description="How often patient gets needed emotional support")

class PsychosocialHealth(BaseModel):
    distressing_feelings: Optional[Frequency] = Field(None, description="Frequency of feelings causing distress or social interference")
    stress_levels: Optional[Frequency] = Field(None, description="Frequency of stress over health, finances, relationships, work")
    body_pain: Optional[Frequency] = Field(None, description="Frequency of body pain")
    fatigue: Optional[Frequency] = Field(None, description="Frequency of fatigue")

class HealthHabits(BaseModel):
    exercise_days_per_week: Optional[int] = Field(None, description="Number of days exercised in past 7 days")
    exercise_minutes: Optional[int] = Field(None, description="Minutes of exercise on days when exercised")
    exercise_intensity: Optional[ExerciseIntensity] = Field(None, description="Typical exercise intensity")
    fruits_vegetables_frequency: Optional[Frequency] = Field(None, description="Frequency of eating 3+ servings fruits/vegetables daily")
    high_fiber_frequency: Optional[Frequency] = Field(None, description="Frequency of eating 3+ servings high fiber/whole grain foods daily")
    mouth_teeth_condition: Optional[HealthRating] = Field(None, description="Condition of mouth and teeth")
    hearing_trouble: Optional[YesNo] = Field(None, description="Trouble hearing people speak")
    wears_hearing_aid: Optional[YesNo] = Field(None, description="Wears hearing aid or device")
    uses_seatbelt: Optional[YesNo] = Field(None, description="Always uses seatbelt in car")
    has_fire_extinguisher: Optional[YesNo] = Field(None, description="Has fire extinguisher in home")
    has_smoke_detector: Optional[YesNo] = Field(None, description="Has smoke detector")

class FunctionMobility(BaseModel):
    # Basic ADLs
    preparing_food_eating: Optional[AbilityLevel] = Field(None, description="Ability to prepare food and eat")
    bathing: Optional[AbilityLevel] = Field(None, description="Ability to bathe")
    getting_dressed: Optional[AbilityLevel] = Field(None, description="Ability to get dressed")
    using_toilet: Optional[AbilityLevel] = Field(None, description="Ability to use toilet")
    moving_around: Optional[AbilityLevel] = Field(None, description="Ability to move around from place to place")
    
    # Assistive devices
    assistive_devices: Optional[List[str]] = Field(None, description="List of assistive devices used")
    
    # Safety and falls
    fallen_or_near_fall: Optional[YesNo] = Field(None, description="Has fallen or had near fall in past year")
    afraid_of_falling: Optional[YesNo] = Field(None, description="Afraid of falling")
    balance_issues: Optional[YesNo] = Field(None, description="Issues with balance or feeling unsteady")
    feels_safe_at_home: Optional[YesNo] = Field(None, description="Feels safe in home environment")
    trip_slip_hazards: Optional[YesNo] = Field(None, description="Anything in home that might cause trips or slips")
    
    # Incontinence
    leaks_urine_stool: Optional[YesNo] = Field(None, description="Ever leaks urine or stool")
    wears_protective_liner: Optional[YesNo] = Field(None, description="Wears liner, pad, or special underwear for leakage")
    
    # IADLs
    shopping: Optional[AbilityLevel] = Field(None, description="Ability to shop")
    using_telephone: Optional[AbilityLevel] = Field(None, description="Ability to use telephone")
    housekeeping: Optional[AbilityLevel] = Field(None, description="Ability to do housekeeping")
    laundry: Optional[AbilityLevel] = Field(None, description="Ability to do laundry")
    driving_transportation: Optional[AbilityLevel] = Field(None, description="Ability to drive or use transportation")
    managing_finances: Optional[AbilityLevel] = Field(None, description="Ability to manage finances")
    taking_medications: Optional[AbilityLevel] = Field(None, description="Ability to take medications")

class MemoryAssessment(BaseModel):
    memory_issues: Optional[YesNo] = Field(None, description="Has experienced memory issues or thinking problems")
    concerns_raised_by_others: Optional[YesNo] = Field(None, description="Have others raised concerns about memory")

class ScreeningTest(BaseModel):
    where_completed: Optional[str] = Field(None, description="Where screening was completed")
    when_completed: Optional[str] = Field(None, description="When screening was completed")
    results_normal: Optional[NormalResults] = Field(None, description="Were results normal")

class PreventiveServices(BaseModel):
    pneumococcal_vaccine: Optional[ScreeningTest] = Field(None, description="Pneumococcal vaccine information")
    influenza_vaccine: Optional[ScreeningTest] = Field(None, description="Influenza vaccine information")
    hepatitis_b_vaccine: Optional[ScreeningTest] = Field(None, description="Hepatitis B vaccine information")
    mammogram: Optional[ScreeningTest] = Field(None, description="Mammogram screening information")
    pap_smear: Optional[ScreeningTest] = Field(None, description="Pap smear information")
    colorectal_screening: Optional[ScreeningTest] = Field(None, description="Colorectal cancer screening information")
    diabetes_screening: Optional[ScreeningTest] = Field(None, description="Diabetes screening information")
    cholesterol_panel: Optional[ScreeningTest] = Field(None, description="Cholesterol panel information")
    bone_density: Optional[ScreeningTest] = Field(None, description="Bone density screening information")
    eye_exam: Optional[ScreeningTest] = Field(None, description="Eye exam information")
    aaa_screening: Optional[ScreeningTest] = Field(None, description="Abdominal aortic aneurysm screening information")

class AdvanceCareActions(BaseModel):
    has_polst: Optional[DontKnow] = Field(None, description="Has POLST form")
    has_living_will: Optional[DontKnow] = Field(None, description="Has living will or advance directive")
    has_power_of_attorney: Optional[DontKnow] = Field(None, description="Has durable power of attorney for medical affairs")
    wants_to_discuss: Optional[YesNo] = Field(None, description="Wants to discuss advance care planning")

class WellnessVisitForm(BaseModel):
    """Medicare Annual Wellness Visit Health Risk Assessment form data"""
    
    basic_info: Optional[BasicInfo] = Field(None, description="Basic patient information")
    care_providers: Optional[CareProviders] = Field(None, description="Outside care providers")
    self_assessment: Optional[SelfAssessment] = Field(None, description="Self assessment of health")
    psychosocial_health: Optional[PsychosocialHealth] = Field(None, description="Psychosocial health assessment")
    health_habits: Optional[HealthHabits] = Field(None, description="Health and habits assessment")
    function_mobility: Optional[FunctionMobility] = Field(None, description="Function and mobility assessment")
    memory_assessment: Optional[MemoryAssessment] = Field(None, description="Signs of memory issues")
    preventive_services: Optional[PreventiveServices] = Field(None, description="Screening and preventive services")
    advance_care_planning: Optional[AdvanceCareActions] = Field(None, description="Advance care planning")

# Sample transcript for Medicare Wellness Visit
sample_wellness_transcript = """
MEDICARE WELLNESS VISIT INTERVIEW
Date: June 18, 2025

NURSE: Good morning, Mrs. Johnson. I need to complete your Medicare Annual Wellness Visit assessment today.

NURSE: Let me confirm your information. Your name is Margaret Johnson?
PATIENT: Yes, that's correct.

NURSE: Date of birth is September 12, 1950?
PATIENT: Yes, I'm 74 years old.

NURSE: Do you have any care providers outside of UW Medicine that we should know about?
PATIENT: Yes, I see Dr. Smith, an eye doctor at Vision Care Center, and I go to Dr. Brown, a podiatrist at Foot Health Clinic.

NURSE: How would you rate your overall health in the past 4 weeks?
PATIENT: I'd say it's good. I've been feeling pretty well overall.

NURSE: Can you manage your overall health problems?
PATIENT: Yes, I think I do a good job managing my diabetes and blood pressure.

NURSE: Do you need help from another person with personal care like eating, bathing, or dressing?
PATIENT: No, I can still do all that myself.

NURSE: Do you often get the emotional support you need?
PATIENT: Usually. My family is pretty good about checking on me.

NURSE: In the past 2 weeks, how often have you been bothered by feelings that caused distress or interfered with getting along with family or friends?
PATIENT: Not at all, really.

NURSE: How about stress over health, finances, relationships, or work?
PATIENT: Several days. I worry about my medical bills sometimes.

NURSE: Any body pain?
PATIENT: Several days. My arthritis acts up sometimes.

NURSE: Fatigue?
PATIENT: Not at all. I have good energy.

NURSE: In the past 7 days, how many days did you exercise?
PATIENT: I walked 4 days this week.

NURSE: On the days you exercised, about how long?
PATIENT: About 30 minutes each time.

NURSE: How intense was your exercise?
PATIENT: I'd say moderate - a brisk walk around the neighborhood.

NURSE: How often did you eat 3 or more servings of fruits and vegetables daily?
PATIENT: Nearly every day. I try to eat healthy.

NURSE: How about high fiber or whole grain foods?
PATIENT: More than half the days, I'd say.

NURSE: How would you describe the condition of your mouth and teeth?
PATIENT: Good. I have some dentures but they fit well.

NURSE: Do you have trouble hearing people speak?
PATIENT: Yes, sometimes I have to ask people to repeat themselves.

NURSE: Do you wear a hearing aid?
PATIENT: No, not yet.

NURSE: Do you always use your seatbelt in the car?
PATIENT: Yes, always.

NURSE: Do you have a fire extinguisher in your home?
PATIENT: Yes.

NURSE: Smoke detector?
PATIENT: Yes, we check the batteries regularly.

NURSE: Can you prepare food and eat by yourself?
PATIENT: Yes, I can do that myself.

NURSE: How about bathing?
PATIENT: I can do it myself, though I'm a bit slower than I used to be.

NURSE: Getting dressed?
PATIENT: I can do that myself.

NURSE: Using the toilet?
PATIENT: Yes, no problems there.

NURSE: Moving around from place to place?
PATIENT: I can do it myself, but I use a cane sometimes for longer walks.

NURSE: Do you use any assistive devices?
PATIENT: Just a cane occasionally.

NURSE: Have you fallen or had a near fall in the past year?
PATIENT: Yes, I slipped on some ice last winter but didn't get hurt badly.

NURSE: Are you afraid of falling?
PATIENT: Yes, a little. That ice incident made me more careful.

NURSE: Do you have issues with balance?
PATIENT: Sometimes, especially when I get up too quickly.

NURSE: Do you feel safe in your home?
PATIENT: Yes, very safe.

NURSE: Anything that might make you trip or slip?
PATIENT: I moved some throw rugs after my fall.

NURSE: Do you ever leak urine or stool?
PATIENT: Occasionally, just a little urine.

NURSE: Do you wear any protective pads?
PATIENT: Yes, I wear a light liner sometimes.

NURSE: Can you do your shopping by yourself?
PATIENT: I need some help. My daughter takes me grocery shopping.

NURSE: Using the telephone?
PATIENT: I can do that myself.

NURSE: Housekeeping?
PATIENT: I need some help with the heavier cleaning.

NURSE: Laundry?
PATIENT: I can do that myself.

NURSE: Driving or using transportation?
PATIENT: I still drive during the day, but my daughter drives at night.

NURSE: Managing your finances?
PATIENT: I can do that myself.

NURSE: Taking your medications?
PATIENT: I can do that myself. I use a pill organizer.

NURSE: Have you experienced any memory issues?
PATIENT: Sometimes I forget where I put things, but nothing major.

NURSE: Have family or friends raised concerns about your memory?
PATIENT: No, they haven't said anything.

NURSE: Let's review your preventive care. When was your last flu shot?
PATIENT: I got it at Walgreens last October, in 2024.

NURSE: Was it normal?
PATIENT: Yes, no problems.

NURSE: Mammogram?
PATIENT: I had one at Imaging Center last year in March 2024. It was normal.

NURSE: Colonoscopy?
PATIENT: I had one at Endoscopy Associates in 2022. It was normal.

NURSE: Diabetes screening?
PATIENT: My blood sugar was checked here last month. It was a little high but not too bad.

NURSE: Cholesterol?
PATIENT: Checked here last month too. Dr. Williams said it was okay.

NURSE: Bone density test?
PATIENT: I had one at Radiology Plus two years ago. It showed some osteoporosis.

NURSE: Eye exam?
PATIENT: I see Dr. Smith every year. Last visit was in January 2025. He said I need stronger glasses.

NURSE: Do you have a POLST form?
PATIENT: I don't think so. I'm not sure what that is.

NURSE: How about a living will or advance directive?
PATIENT: Yes, I have one.

NURSE: Durable power of attorney for medical decisions?
PATIENT: Yes, my daughter has that.

NURSE: Would you like to discuss advance care planning today?
PATIENT: Not sure. Maybe we could talk about it briefly.
"""

WELLNESS_VISIT_CLINICAL_WEIGHTS = {
    # Critical - patient identification
    "basic_info.name": 2.5,
    "basic_info.birthdate": 2.0,
    "basic_info.todays_date": 1.0,
    
    # Important - health status
    "self_assessment.overall_health_rating": 2.0,
    "self_assessment.can_manage_health_problems": 2.0,
    "self_assessment.needs_help_personal_care": 2.5,
    "function_mobility.fallen_or_near_fall": 2.5,
    "function_mobility.afraid_of_falling": 2.0,
    "function_mobility.balance_issues": 2.5,
    "memory_assessment.memory_issues": 2.5,
    "memory_assessment.concerns_raised_by_others": 2.0,
    
    # Important - functional status
    "function_mobility.bathing": 2.0,
    "function_mobility.getting_dressed": 2.0,
    "function_mobility.using_toilet": 2.0,
    "function_mobility.preparing_food_eating": 2.0,
    "function_mobility.moving_around": 2.0,
    "function_mobility.taking_medications": 2.5,
    "function_mobility.managing_finances": 1.5,
    "function_mobility.driving_transportation": 1.5,
    
    # Health habits - moderate importance
    "health_habits.exercise_days_per_week": 1.5,
    "health_habits.exercise_minutes": 1.5,
    "health_habits.exercise_intensity": 1.5,
    "health_habits.fruits_vegetables_frequency": 1.5,
    "health_habits.hearing_trouble": 2.0,
    "health_habits.uses_seatbelt": 1.0,
    
    # Preventive services - important
    "preventive_services.mammogram": 2.0,
    "preventive_services.colorectal_screening": 2.0,
    "preventive_services.diabetes_screening": 2.0,
    "preventive_services.cholesterol_panel": 2.0,
    "preventive_services.bone_density": 2.0,
    "preventive_services.eye_exam": 1.5,
    
    # Advance care planning - important
    "advance_care_planning.has_living_will": 2.0,
    "advance_care_planning.has_power_of_attorney": 2.0,
    "advance_care_planning.has_polst": 1.5,
    "advance_care_planning.wants_to_discuss": 1.0,
    
    # Supporting information
    "care_providers.outside_providers": 1.0,
    "self_assessment.emotional_support": 1.5,
    "psychosocial_health.distressing_feelings": 1.5,
    "psychosocial_health.stress_levels": 1.5,
    "psychosocial_health.body_pain": 1.5,
    "psychosocial_health.fatigue": 1.5,
    "health_habits.high_fiber_frequency": 1.0,
    "health_habits.mouth_teeth_condition": 1.0,
    "health_habits.wears_hearing_aid": 1.5,
    "health_habits.has_fire_extinguisher": 1.0,
    "health_habits.has_smoke_detector": 1.0,
    "function_mobility.assistive_devices": 1.5,
    "function_mobility.feels_safe_at_home": 1.5,
    "function_mobility.trip_slip_hazards": 1.5,
    "function_mobility.leaks_urine_stool": 1.5,
    "function_mobility.wears_protective_liner": 1.0,
    "function_mobility.shopping": 1.5,
    "function_mobility.using_telephone": 1.0,
    "function_mobility.housekeeping": 1.0,
    "function_mobility.laundry": 1.0
}