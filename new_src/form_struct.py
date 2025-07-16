from typing import List, Optional, Union, Any
from pydantic import BaseModel, Field
from enum import Enum

class FieldType(str, Enum):
    TEXT_INPUT = "text_input"
    DATE = "date"
    CHECKBOX = "checkbox"
    DROPDOWN = "dropdown"
    TEXTAREA = "textarea"
    NUMBER = "number"
    EMAIL = "email"
    PHONE = "phone"
    RADIO = "radio"

class FormField(BaseModel):
    field_name: str = Field(..., description="Unique identifier for the field")
    field_type: FieldType = Field(..., description="Type of form field")
    label: str = Field(..., description="Human-readable label for the field")
    required: bool = Field(default=False, description="Whether field is required")
    value: Optional[Union[str, int, float, bool, List[str]]] = Field(
        default=None, 
        description="Extracted value from transcript or null if not found"
    )
    options: Optional[List[str]] = Field(
        default=None, 
        description="Available options for dropdown/radio fields"
    )
    source_quote: Optional[str] = Field(
        default=None, 
        description="Exact quote from transcript used to fill this field"
    )

class FormStructure(BaseModel):
    #section_id: int = Field(..., description="Unique identifier for the section")
    fields: List[FormField] = Field(..., description="List of form fields with filled values")


# if using pydantic for disjoint sections
class DisjointSections(BaseModel):
    sections: List[List[int]] = Field(
        ..., 
        description="Array of arrays where each subarray contains chunk indices that represent separate, independent sections of the form that can be processed in parallel"
    )