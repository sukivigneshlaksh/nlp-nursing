"""
Extracted Syntax Patterns and Code Snippets from Archive and Recent_Work Directories

This file contains meaningful syntax patterns, architectural approaches, and code structures
extracted from the archive and recent_work directories for future reference.
"""

from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, BeforeValidator
from typing_extensions import Annotated
import fitz
import streamlit as st


# =============================================================================
# MEDICAL DOMAIN MODELING PATTERNS
# =============================================================================

class YesNoUnknown(str, Enum):
    """Standard medical yes/no/unknown enum"""
    yes = "Yes"
    no = "No"
    unknown = "Unknown"


class TemperatureSite(str, Enum):
    """Temperature measurement sites"""
    oral = "Oral"
    rectal = "Rectal"
    axillary = "Axillary"
    tympanic = "Tympanic"
    temporal = "Temporal"


class PulsePosition(str, Enum):
    """Patient positions during pulse measurement"""
    sitting = "Sitting"
    lying = "Lying"
    standing = "Standing"


class VitalSigns(BaseModel):
    """Medical vital signs data structure"""
    temperature_f: Optional[float] = Field(None, description="Temperature in Fahrenheit")
    temperature_site: Optional[TemperatureSite] = Field(None, description="Site of temperature measurement")
    pulse_bpm: Optional[int] = Field(None, description="Pulse rate in beats per minute")
    pulse_position: Optional[PulsePosition] = Field(None, description="Patient position during pulse measurement")
    blood_pressure_systolic: Optional[int] = Field(None, description="Systolic blood pressure")
    blood_pressure_diastolic: Optional[int] = Field(None, description="Diastolic blood pressure")
    respiratory_rate: Optional[int] = Field(None, description="Respiratory rate per minute")
    oxygen_saturation: Optional[float] = Field(None, description="Oxygen saturation percentage")


class PhysicalExamination(BaseModel):
    """Complete physical examination structure"""
    vitals: Optional[VitalSigns] = Field(None, description="Vital signs")
    general_appearance: Optional[str] = Field(None, description="General appearance assessment")
    head_examination: Optional[str] = Field(None, description="Head examination findings")
    cardiovascular: Optional[str] = Field(None, description="Cardiovascular examination")
    respiratory: Optional[str] = Field(None, description="Respiratory examination")
    neurological: Optional[str] = Field(None, description="Neurological examination")


class Medication(BaseModel):
    """Medication information model"""
    name: Optional[str] = Field(None, description="Medication name")
    dosage: Optional[str] = Field(None, description="Medication dosage")
    frequency: Optional[str] = Field(None, description="Frequency of administration")
    purpose: Optional[str] = Field(None, description="Purpose/reason for medication")
    route: Optional[str] = Field(None, description="Route of administration")


# =============================================================================
# DATA VALIDATION PATTERNS
# =============================================================================

def fix_height(value):
    """Convert feet to inches if needed"""
    if value is None:
        return None
    if value < 10:
        return value * 12  # Convert feet to inches
    return value


def fix_weight(value):
    """Validate and normalize weight values"""
    if value is None:
        return None
    if value < 50:
        return None  # Likely invalid weight
    return value


class PatientInfo(BaseModel):
    """Patient information with validation"""
    height_inches: Annotated[Optional[int], BeforeValidator(fix_height)] = None
    weight_pounds: Annotated[Optional[int], BeforeValidator(fix_weight)] = None
    age: Optional[int] = Field(None, ge=0, le=150, description="Patient age in years")
    gender: Optional[str] = Field(None, description="Patient gender")


# =============================================================================
# AGENT-BASED ARCHITECTURE PATTERNS
# =============================================================================

class BaseFormAgent(ABC):
    """Abstract base class for form processing agents"""
    
    def __init__(self, output_dir: str = "outputs", load_env: bool = True, 
                 project_id: str = "suki-dev", location: str = "us-central1"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.project_id = project_id
        self.location = location
        
        if load_env:
            self._load_environment()
    
    def _load_environment(self):
        """Load environment variables and configure services"""
        try:
            # Load environment configuration
            pass
        except Exception as e:
            print(f"Failed to load environment: {e}")
    
    def _configure_vertex_ai(self):
        """Configure Vertex AI client"""
        try:
            # Configure Vertex AI
            pass
        except Exception as e:
            print(f"Failed to configure Vertex AI: {e}")
    
    def is_gemini_model(self, model_string: str) -> bool:
        """Check if model is a Gemini model"""
        return (model_string.startswith("vertex:gemini") or 
                model_string.startswith("gemini") or
                "gemini" in model_string.lower())
    
    @abstractmethod
    def process_form(self, input_data: Any) -> Any:
        """Process form data - must be implemented by subclasses"""
        pass


class PDFExtractionAgent(BaseFormAgent):
    """Agent for extracting data from PDF forms"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.system_prompt = """You are an expert medical form field extractor with 10+ years experience analyzing healthcare documents."""
    
    def extract_chunk_region(self, pdf_path: str, chunk) -> Optional[bytes]:
        """Extract a specific region from PDF as image"""
        try:
            doc = fitz.open(pdf_path)
            page = doc[chunk.page_number]
            page_rect = page.rect
            
            # Convert normalized coordinates (0-1) to actual pixel coordinates
            actual_box = fitz.Rect(
                chunk.bounding_box.l * page_rect.width,   # left
                chunk.bounding_box.t * page_rect.height,  # top
                chunk.bounding_box.r * page_rect.width,   # right
                chunk.bounding_box.b * page_rect.height   # bottom
            )
            
            # Extract the region as high-quality image
            pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72), clip=actual_box)
            return pix.tobytes("png")
        except Exception as e:
            print(f"Error extracting chunk region: {e}")
            return None


# =============================================================================
# MULTI-MODEL INTEGRATION PATTERNS
# =============================================================================

def text_to_pydantic_with_gold(fields_text: str, model_client) -> str:
    """Convert text to Pydantic model with golden standard examples"""
    
    golden_standard_prompt = """GOLDEN STANDARD EXAMPLE:
class Medication(BaseModel):
    name: Optional[str] = Field(None, description="Medication name")
    purpose: Optional[str] = Field(None, description="Purpose/reason for medication")
    
OUTPUT: Pure Python code only, no explanations or markdown."""
    
    prompt = f"{golden_standard_prompt}\n\nNow convert this to Pydantic:\n{fields_text}"
    
    try:
        # Check model type and call appropriate API
        if hasattr(model_client, 'chat'):  # OpenAI
            response = model_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        else:  # Vertex AI
            response = model_client.generate_content(prompt)
            return response.text
    except Exception as e:
        print(f"Error in model generation: {e}")
        return ""


def create_model_configs():
    """Create configuration for multi-model testing"""
    return [
        ("openai", "with_gold", "openai_client", "openai_fields", text_to_pydantic_with_gold),
        ("openai", "without_gold", "openai_client", "openai_fields", "text_to_pydantic_without_gold"),
        ("vertex", "with_gold", "gemini_model", "vertex_fields", text_to_pydantic_with_gold),
        ("vertex", "without_gold", "gemini_model", "vertex_fields", "text_to_pydantic_without_gold")
    ]


# =============================================================================
# EVALUATION AND SCORING PATTERNS
# =============================================================================

def evaluate_extraction_with_weights(extracted_data, transcript, weights):
    """Evaluate extraction quality with clinical weights using field-level weights"""
    field_evaluations = {}
    weighted_total = 0
    weight_sum = 0
    
    # Flatten data to match weight keys
    flattened_data = flatten_data_for_weights(extracted_data.model_dump())
    
    for field_path, weight in weights.items():
        field_value = flattened_data.get(field_path)
        if field_value is not None:
            score = evaluate_field(field_path, field_value, transcript)
            weighted_score = score * weight
            weighted_total += weighted_score
            weight_sum += weight
            field_evaluations[field_path] = {
                'value': field_value,
                'score': score,
                'weight': weight,
                'weighted_score': weighted_score
            }
    
    overall_score = weighted_total / weight_sum if weight_sum > 0 else 0
    
    return {
        'overall_score': overall_score,
        'field_evaluations': field_evaluations,
        'total_weighted_score': weighted_total,
        'total_weight': weight_sum
    }


def flatten_data_for_weights(data_dict):
    """Convert nested dict to flat keys matching weight structure"""
    flattened = {}
    
    def _flatten(obj, prefix=""):
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_key = f"{prefix}.{key}" if prefix else key
                if isinstance(value, dict):
                    _flatten(value, new_key)
                elif isinstance(value, list):
                    for i, item in enumerate(value):
                        if isinstance(item, dict):
                            _flatten(item, f"{new_key}[{i}]")
                        else:
                            flattened[f"{new_key}[{i}]"] = item
                else:
                    flattened[new_key] = value
        else:
            flattened[prefix] = obj
    
    _flatten(data_dict)
    return flattened


def evaluate_field(field_path, field_value, transcript):
    """Evaluate a single field's extraction quality"""
    # Simple scoring logic - can be enhanced with more sophisticated methods
    if field_value is None or field_value == "":
        return 0.0
    
    # Check if field value appears in transcript (basic relevance check)
    if str(field_value).lower() in transcript.lower():
        return 1.0
    
    # Partial matching for complex fields
    words = str(field_value).lower().split()
    matches = sum(1 for word in words if word in transcript.lower())
    return matches / len(words) if words else 0.0


# =============================================================================
# STREAMLIT UI PATTERNS
# =============================================================================

def format_field_name(field_name: str) -> str:
    """Format field names for display"""
    return field_name.replace('_', ' ').title()


def display_field(key, value, level=0):
    """Display a single field with proper formatting"""
    if value is None:
        return
    
    indent = "  " * level
    
    if isinstance(value, BaseModel):
        st.markdown(f"**{format_field_name(key)}**")
        display_model(value, level + 1)
    elif isinstance(value, list):
        if not value:
            return
        st.markdown(f"**{format_field_name(key)}:**")
        for i, item in enumerate(value):
            if isinstance(item, BaseModel):
                st.markdown(f"{indent}**Item {i + 1}:**")
                display_model(item, level + 1)
            else:
                st.markdown(f"{indent}- {item}")
    elif isinstance(value, dict):
        st.markdown(f"**{format_field_name(key)}:**")
        for sub_key, sub_value in value.items():
            display_field(sub_key, sub_value, level + 1)
    else:
        st.markdown(f"**{format_field_name(key)}:** {value}")


def display_model(model: BaseModel, level=0):
    """Recursively display a Pydantic model"""
    for field_name, field_value in model.model_dump().items():
        if field_value is not None:
            display_field(field_name, field_value, level)


def create_form_configuration():
    """Create form configuration for Streamlit app"""
    return {
        "Medical History": {
            "model": "MedicalHistoryForm",
            "transcript": "sample_transcript",
            "status": "active",
            "display_func": "display_medical_history"
        },
        "CMS PAP Device": {
            "model": "CMSPAPDeviceForm",
            "transcript": "sample_transcript",
            "status": "active",
            "display_func": "display_cms_results"
        },
        "Pain Assessment": {
            "model": "PainAssessmentForm",
            "transcript": "sample_transcript",
            "status": "active",
            "display_func": "display_pain_assessment"
        }
    }


def get_display_function(form_name):
    """Return appropriate display function based on form type"""
    display_functions = {
        "Medical History": display_model,
        "CMS PAP Device": display_model,
        "Pain Assessment": display_model
    }
    return display_functions.get(form_name, display_model)


# =============================================================================
# ADVANCED PDF PROCESSING PATTERNS
# =============================================================================

class ChunkExtraction(BaseModel):
    """Data structure for PDF chunk extraction"""
    page_number: int
    text_content: str
    bounding_box: Dict[str, float]  # {"l": left, "t": top, "r": right, "b": bottom}
    confidence: Optional[float] = None


def extract_pdf_regions_with_vision(pdf_path: str, chunks: List[ChunkExtraction]) -> List[bytes]:
    """Extract specific regions from PDF using vision processing"""
    extracted_regions = []
    
    try:
        doc = fitz.open(pdf_path)
        
        for chunk in chunks:
            page = doc[chunk.page_number]
            page_rect = page.rect
            
            # Convert normalized coordinates to actual coordinates
            actual_box = fitz.Rect(
                chunk.bounding_box["l"] * page_rect.width,
                chunk.bounding_box["t"] * page_rect.height,
                chunk.bounding_box["r"] * page_rect.width,
                chunk.bounding_box["b"] * page_rect.height
            )
            
            # Extract high-quality image
            matrix = fitz.Matrix(300/72, 300/72)  # 300 DPI
            pix = page.get_pixmap(matrix=matrix, clip=actual_box)
            extracted_regions.append(pix.tobytes("png"))
        
        doc.close()
        return extracted_regions
        
    except Exception as e:
        print(f"Error extracting PDF regions: {e}")
        return []


# =============================================================================
# CLINICAL WEIGHT CONFIGURATIONS
# =============================================================================

def get_clinical_weights():
    """Return clinical importance weights for different medical fields"""
    return {
        "patient_demographics.age": 0.8,
        "patient_demographics.gender": 0.6,
        "vital_signs.blood_pressure_systolic": 0.9,
        "vital_signs.blood_pressure_diastolic": 0.9,
        "vital_signs.heart_rate": 0.85,
        "vital_signs.temperature": 0.7,
        "medications.name": 0.95,
        "medications.dosage": 0.9,
        "medications.frequency": 0.85,
        "allergies.medication": 0.95,
        "allergies.severity": 0.9,
        "chief_complaint": 0.95,
        "history_of_present_illness": 0.9,
        "past_medical_history": 0.8,
        "family_history": 0.6,
        "social_history.smoking": 0.7,
        "social_history.alcohol": 0.7,
        "review_of_systems": 0.75,
        "physical_examination.general": 0.8,
        "physical_examination.cardiovascular": 0.85,
        "physical_examination.respiratory": 0.85,
        "physical_examination.neurological": 0.8,
        "assessment_and_plan": 0.95
    }


# =============================================================================
# ERROR HANDLING AND LOGGING PATTERNS
# =============================================================================

def safe_model_call(func, *args, **kwargs):
    """Safely call model with error handling"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"Error in model call: {e}")
        return None


def log_processing_metrics(start_time, end_time, success_count, error_count):
    """Log processing metrics for monitoring"""
    duration = end_time - start_time
    total_processed = success_count + error_count
    success_rate = success_count / total_processed if total_processed > 0 else 0
    
    metrics = {
        "processing_duration": duration,
        "total_processed": total_processed,
        "success_count": success_count,
        "error_count": error_count,
        "success_rate": success_rate,
        "throughput": total_processed / duration if duration > 0 else 0
    }
    
    return metrics


# =============================================================================
# CONFIGURATION MANAGEMENT PATTERNS
# =============================================================================

class ProcessingConfig(BaseModel):
    """Configuration for form processing"""
    model_provider: str = "openai"
    model_name: str = "gpt-4o"
    max_retries: int = 3
    timeout_seconds: int = 30
    use_golden_standard: bool = True
    output_format: str = "json"
    enable_validation: bool = True
    confidence_threshold: float = 0.8


def load_config_from_env():
    """Load configuration from environment variables"""
    import os
    
    return ProcessingConfig(
        model_provider=os.getenv("MODEL_PROVIDER", "openai"),
        model_name=os.getenv("MODEL_NAME", "gpt-4o"),
        max_retries=int(os.getenv("MAX_RETRIES", "3")),
        timeout_seconds=int(os.getenv("TIMEOUT_SECONDS", "30")),
        use_golden_standard=os.getenv("USE_GOLDEN_STANDARD", "true").lower() == "true",
        output_format=os.getenv("OUTPUT_FORMAT", "json"),
        enable_validation=os.getenv("ENABLE_VALIDATION", "true").lower() == "true",
        confidence_threshold=float(os.getenv("CONFIDENCE_THRESHOLD", "0.8"))
    )


# =============================================================================
# SAMPLE USAGE PATTERNS
# =============================================================================

def example_medical_form_processing():
    """Example of how to use the extracted patterns"""
    
    # Create patient info with validation
    patient = PatientInfo(
        height_inches=70,  # Will be validated
        weight_pounds=180,  # Will be validated
        age=45,
        gender="Male"
    )
    
    # Create vital signs
    vitals = VitalSigns(
        temperature_f=98.6,
        temperature_site=TemperatureSite.oral,
        pulse_bpm=72,
        pulse_position=PulsePosition.sitting,
        blood_pressure_systolic=120,
        blood_pressure_diastolic=80
    )
    
    # Create medication record
    medication = Medication(
        name="Lisinopril",
        dosage="10mg",
        frequency="Once daily",
        purpose="Blood pressure control",
        route="Oral"
    )
    
    # Example of weighted evaluation
    sample_data = {
        "patient_demographics": {"age": 45, "gender": "Male"},
        "vital_signs": {"blood_pressure_systolic": 120, "heart_rate": 72},
        "medications": [{"name": "Lisinopril", "dosage": "10mg"}]
    }
    
    weights = get_clinical_weights()
    transcript = "45 year old male with blood pressure 120/80, heart rate 72, taking Lisinopril 10mg daily"
    
    # This would evaluate the extraction quality
    # evaluation = evaluate_extraction_with_weights(sample_data, transcript, weights)
    
    return {
        "patient": patient,
        "vitals": vitals,
        "medication": medication
    }


if __name__ == "__main__":
    print("Extracted syntax patterns loaded successfully!")
    print("This file contains reusable patterns for medical form processing and NLP applications.")