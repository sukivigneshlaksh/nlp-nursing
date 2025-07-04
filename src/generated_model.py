from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import date

class Medication(BaseModel):
    name: str = Field(description="Name of medication")
    purpose: str = Field(description="Purpose of medication")

class Hospitalization(BaseModel):
    hospital: str = Field(description="Name of hospital")
    date: Optional[date] = Field(description="Date of hospitalization")
    reason: str = Field(description="Reason for hospitalization")

class Surgery(BaseModel):
    surgery: str = Field(description="Type of surgery")
    date: Optional[date] = Field(description="Date of surgery")


class MedicalHistory(BaseModel):
    name: str = Field(description="Patient's name")
    age: Optional[int] = Field(description="Patient's age")
    date: Optional[date] = Field(description="Date of form completion")
    county_of_residence: str = Field(description="Patient's county of residence")
    major_medical_problems: str = Field(description="List of major medical problems")
    current_doctor: str = Field(description="Patient's current doctor")
    medications: List[Medication] = Field(description="List of current medications", default=[])
    hospitalizations: List[Hospitalization] = Field(description="List of hospitalizations (recent to earliest)", default=[])
    surgeries: List[Surgery] = Field(description="List of surgeries (recent to earliest)", default=[])
