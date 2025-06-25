from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class PainLocation(str, Enum):
    generalized = "Generalized"
    head = "Head"
    neck = "Neck"
    shoulder = "Shoulder"
    back = "Back"
    upper_back = "Upper Back"
    lower_back = "Lower Back"
    arm = "Arm"
    hand = "Hand"
    chest = "Chest"
    breast = "Breast"
    abdomen = "Abdomen"
    coccyx = "Coccyx"
    buttocks = "Buttocks"
    hip = "Hip"
    leg = "Leg"
    knee = "Knee"
    ankle = "Ankle"
    foot = "Foot"
    heel = "Heel"
    joint = "Joint"

class PainLocationInfo(BaseModel):
    location: Optional[PainLocation] = Field(None, description="Primary location of pain (dropdown)")
    area: Optional[str] = Field(None, description="Area specification - free text")
    description: Optional[str] = Field(None, description="Specific description of pain location - free text")

class PainHistoryInfo(BaseModel):
    history: Optional[str] = Field(None, description="Pain history - free text")
    most_recent_episode: Optional[str] = Field(None, description="Most recent episode details - free text")
    most_recent_episode_duration: Optional[str] = Field(None, description="Duration of most recent episode - free text")
    most_recent_episode_details: Optional[str] = Field(None, description="Additional details about most recent episode - free text")

class PainCurrentCondition(BaseModel):
    current_condition_status: Optional[str] = Field(None, description="Current pain condition status - free text")
    status_change: Optional[str] = Field(None, description="How pain status is changing - free text")
    severity: Optional[str] = Field(None, description="Pain severity level - free text")

class PainScale(BaseModel):
    score: Optional[str] = Field(None, description="Pain scale score - free text")
    rating_omitted: Optional[str] = Field(None, description="Reason if pain rating was omitted - free text")

class PainFactors(BaseModel):
    aggravating_factors: Optional[str] = Field(None, description="Factors that make pain worse - free text")
    precipitating_factors: Optional[str] = Field(None, description="Factors that trigger pain - free text")
    relieving_factors: Optional[str] = Field(None, description="Factors that relieve pain - free text")

class PainBehavioral(BaseModel):
    behavioral_reactions: Optional[str] = Field(None, description="Observable behavioral reactions to pain - free text")

class PainCharacter(BaseModel):
    onset: Optional[str] = Field(None, description="How pain onset occurred - free text")
    onset_speed: Optional[str] = Field(None, description="Speed of pain onset - free text")
    onset_when: Optional[str] = Field(None, description="Time of day pain typically occurs - free text")
    frequency: Optional[str] = Field(None, description="How often pain occurs - free text")
    duration: Optional[str] = Field(None, description="How long pain episodes last - free text")
    quality: Optional[str] = Field(None, description="Quality/character of the pain - free text")
    radiates: Optional[str] = Field(None, description="Where pain radiates to - free text")
    refers: Optional[str] = Field(None, description="Where pain refers to - free text")
    related_to: Optional[str] = Field(None, description="What pain is related to - free text")
    interferes_with: Optional[str] = Field(None, description="What pain interferes with - free text")

class PainAssessmentForm(BaseModel):
    """Pain Assessment Care Step form data"""
    
    # Pain Location section
    pain_location: Optional[PainLocationInfo] = Field(None, description="Pain location information")
    
    # History section
    pain_history: Optional[PainHistoryInfo] = Field(None, description="Pain history information")
    
    # Current Condition section
    current_condition: Optional[PainCurrentCondition] = Field(None, description="Current pain condition")
    
    # Pain Scale section
    pain_scale: Optional[PainScale] = Field(None, description="Pain scale assessment")
    
    # Factors section
    factors: Optional[PainFactors] = Field(None, description="Pain aggravating, precipitating, and relieving factors")
    
    # Behavioral section
    behavioral: Optional[PainBehavioral] = Field(None, description="Behavioral reactions to pain")
    
    # Associated Symptoms
    associated_symptoms: Optional[str] = Field(None, description="Symptoms associated with pain - free text")
    
    # Character section
    character: Optional[PainCharacter] = Field(None, description="Pain character and timing")
    
    # Intractable and Treatment Response
    intractable: Optional[str] = Field(None, description="Whether pain is intractable - free text")
    treatment_response: Optional[str] = Field(None, description="Response to treatment - free text")
    
    # Note section
    note: Optional[str] = Field(None, description="Additional notes about pain assessment - free text")

# Sample transcript for Pain Assessment form
sample_pain_assessment_transcript = """
PAIN ASSESSMENT INTERVIEW
Date: June 24, 2025
Nurse: Sarah Thompson, RN

NURSE: I need to complete a pain assessment. Can you tell me where you're experiencing pain?
PATIENT: It's mainly in my lower back, but sometimes it goes down my right leg.

NURSE: So the primary location is lower back?
PATIENT: Yes, that's where it hurts the most.

NURSE: And you mentioned it's on the right side and goes down your leg?
PATIENT: Yes, the right side of my lower back, and it shoots down my right leg sometimes.

NURSE: Can you describe the specific location more?
PATIENT: It's right above my tailbone, maybe about 2 inches to the right of my spine.

NURSE: Tell me about the history of this pain. Is this the first time you've had this?
PATIENT: No, I've had back problems for about 5 years, but this episode is worse than usual.

NURSE: When did this most recent episode start?
PATIENT: It started yesterday morning when I was lifting boxes at work.

NURSE: How long has this current episode been lasting?
PATIENT: It's been constant since yesterday morning, so about 30 hours now.

NURSE: Any other details about this episode?
PATIENT: The pain is much sharper than my usual back aches, and the leg pain is new.

NURSE: How would you describe your current pain status?
PATIENT: It's definitely present and pretty bad. The medication isn't helping much.

NURSE: Is the pain getting better, worse, or staying the same?
PATIENT: It's getting worse, especially when I try to sit or stand.

NURSE: How severe would you say the pain is?
PATIENT: I'd say it's severe. It's really interfering with everything I do.

NURSE: On a scale of 0 to 10, what number would you give your pain?
PATIENT: Right now it's about an 8 out of 10.

NURSE: What makes the pain worse?
PATIENT: Sitting, standing, bending forward, and coughing all make it much worse.

NURSE: What brought on this pain episode?
PATIENT: Lifting heavy boxes at work without proper form.

NURSE: What helps relieve the pain?
PATIENT: Lying flat on my back with a pillow under my knees helps a little. Heat therapy too.

NURSE: Have you noticed any behaviors or reactions when the pain is bad?
PATIENT: I catch myself holding my breath and tensing up. I also move very slowly and carefully.

NURSE: Any other symptoms that go along with the pain?
PATIENT: Some muscle spasms in my back and occasional tingling in my right foot.

NURSE: How did the pain start - suddenly or gradually?
PATIENT: It started suddenly when I lifted the box wrong.

NURSE: When during the day is it typically worst?
PATIENT: It's worst in the morning when I first get up and in the evening after being on my feet.

NURSE: How often do you experience this type of pain?
PATIENT: My usual back pain is maybe once a week, but this severe pain is new.

NURSE: How long do episodes typically last?
PATIENT: My regular back pain usually lasts a few hours, but this has been constant.

NURSE: How would you describe the quality of the pain?
PATIENT: It's a sharp, shooting pain with some burning sensations.

NURSE: Does the pain radiate or spread anywhere?
PATIENT: Yes, it shoots down my right leg, sometimes all the way to my foot.

NURSE: Does it seem to refer to any other areas?
PATIENT: Sometimes I feel it in my right hip area too.

NURSE: What do you think this pain is related to?
PATIENT: Definitely the lifting injury at work, but my job requires a lot of heavy lifting.

NURSE: What does this pain interfere with?
PATIENT: Everything - sitting, standing, walking, sleeping, working. Daily activities are very difficult.

NURSE: Would you say this pain is intractable or manageable?
PATIENT: Right now it feels intractable. Nothing I'm doing is really helping.

NURSE: How are you responding to current treatment?
PATIENT: The ibuprofen and muscle relaxer aren't providing much relief. I need something stronger.

NURSE: Any additional notes about your pain?
PATIENT: I'm worried about returning to work. This is affecting my ability to provide for my family.
"""

PAIN_ASSESSMENT_CLINICAL_WEIGHTS = {
    # Critical - pain location and severity
    "pain_location.location": 3.0,
    "pain_scale.score": 3.0,
    "current_condition.severity": 2.5,
    "current_condition.current_condition_status": 2.5,
    
    # Important - pain characteristics
    "character.quality": 2.0,
    "character.onset": 2.0,
    "character.radiates": 2.0,
    "factors.precipitating_factors": 2.0,
    "factors.aggravating_factors": 2.0,
    "factors.relieving_factors": 2.0,
    
    # Clinical assessment
    "pain_history.history": 2.0,
    "pain_history.most_recent_episode": 1.5,
    "current_condition.status_change": 1.5,
    "character.frequency": 1.5,
    "character.duration": 1.5,
    "treatment_response": 2.0,
    
    # Supporting information
    "pain_location.area": 1.5,
    "pain_location.description": 1.0,
    "pain_history.most_recent_episode_duration": 1.0,
    "pain_history.most_recent_episode_details": 1.0,
    "pain_scale.rating_omitted": 1.0,
    "behavioral.behavioral_reactions": 1.0,
    "associated_symptoms": 1.5,
    "character.onset_speed": 1.0,
    "character.onset_when": 1.0,
    "character.refers": 1.0,
    "character.related_to": 1.5,
    "character.interferes_with": 1.5,
    "intractable": 1.5,
    "note": 0.5
}