from pydantic import BaseModel, Field
from typing import Optional, List

class Medication(BaseModel):
    name: Optional[str] = Field(None, description="Name of current medication")
    purpose: Optional[str] = Field(None, description="Purpose of the medication")

class Hospitalization(BaseModel):
    hospital: Optional[str] = Field(None, description="Name of hospital")
    date_text: Optional[str] = Field(None, description="Date of hospitalization as text")
    reason: Optional[str] = Field(None, description="Reason for hospitalization")

class Surgery(BaseModel):
    procedure: Optional[str] = Field(None, description="Type of surgery or procedure")
    date_text: Optional[str] = Field(None, description="Date of surgery as text")

class MedicalHistoryForm(BaseModel):
    """Medical history form data extraction model"""
    
    # Basic information
    name: Optional[str] = Field(None, description="Patient's full name")
    age: Optional[int] = Field(None, description="Patient's age")
    form_date: Optional[str] = Field(None, description="Date form was completed as text")
    county_of_residence: Optional[str] = Field(None, description="County where patient resides")
    
    # Medical problems and history
    major_medical_problems: Optional[List[str]] = Field(None, description="List of major medical problems")
    current_doctor: Optional[str] = Field(None, description="Name of current doctor")
    
    # Current medications
    current_medications: Optional[List[Medication]] = Field(None, description="List of current medications and their purposes")
    
    # Hospitalizations
    hospitalizations: Optional[List[Hospitalization]] = Field(None, description="Recent hospitalizations from most recent to earliest")
    
    # Surgeries
    surgeries: Optional[List[Surgery]] = Field(None, description="Surgeries from most recent to earliest")

# Sample transcript for testing
sample_transcript = """
MEDICAL HISTORY INTAKE
Date: June 18, 2025

NURSE: I need to complete your medical history form. Let's start with your basic information.

NURSE: What's your full name?
PATIENT: John Michael Smith

NURSE: How old are you?
PATIENT: I'm 45 years old.

NURSE: What county do you live in?
PATIENT: I live in Franklin County.

NURSE: Can you tell me about any major medical problems you have?
PATIENT: I have high blood pressure, Type 2 diabetes, and I had a heart attack two years ago.

NURSE: Who is your current doctor?
PATIENT: Dr. Sarah Johnson at Columbus Family Medicine.

NURSE: What medications are you currently taking?
PATIENT: I take Metformin for my diabetes, Lisinopril for blood pressure, and Atorvastatin for cholesterol.

NURSE: Have you been hospitalized recently?
PATIENT: Yes, I was at Ohio State Medical Center in March 2024 for my heart attack. Before that, I was at Mount Carmel in January 2023 for pneumonia.

NURSE: Have you had any surgeries?
PATIENT: I had gallbladder surgery in 2022, and knee arthroscopy in 2020. Oh, and appendectomy when I was 25, so that would be 2005.

NURSE: Can you give me the exact dates for those surgeries?
PATIENT: The gallbladder was September 15, 2022. The knee surgery was June 10, 2020. The appendectomy was sometime in March 2005, I think March 8th.
"""