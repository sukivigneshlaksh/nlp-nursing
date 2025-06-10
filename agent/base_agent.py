import json
import os
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dotenv import load_dotenv
import json

# Vertex AI imports
import vertexai


class BaseFormAgent(ABC):
    
    def __init__(self, output_dir: str = "outputs", load_env: bool = True, 
                 project_id: str = "suki-dev", location: str = "us-central1"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.project_id = project_id
        self.location = location
        
        if load_env:
            load_dotenv()
            self._configure_vertex_ai()
    
    def _configure_vertex_ai(self):
        try:
            # Initialize Vertex AI
            vertexai.init(project=self.project_id, location=self.location)
            print(f"Vertex AI configured for project: {self.project_id}, location: {self.location}")
        except Exception as e:
            print(f"Failed to configure Vertex AI: {e}")
            print("Ensure you're authenticated with: gcloud auth application-default login")
            print("And have the necessary permissions on the project")
    
    def save_json(self, data: Dict[Any, Any], filepath: str) -> str:
        full_path = self.output_dir / filepath
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return str(full_path)
    
    def load_json(self, filepath: str) -> Optional[Dict[Any, Any]]:
        full_path = self.output_dir / filepath
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"File not found: {full_path}")
            return None
        except Exception as e:
            print(f"Error loading {full_path}: {e}")
            return None
    
    def is_gemini_model(self, model_string: str) -> bool:
        return (model_string.startswith("vertex:gemini") or 
                model_string.startswith("gemini") or
                "gemini" in model_string.lower())
    
    def get_gemini_model_name(self, model_string: str) -> str:
        if model_string.startswith("vertex:"):
            return model_string.replace("vertex:", "")
        elif model_string.startswith("gemini"):
            return model_string
        else:
            return "gemini-1.5-flash"
    
    @abstractmethod
    def process(self, pdf_path: str, **kwargs) -> Dict[Any, Any]:
        pass
    
    def get_pdf_name(self, pdf_path: str) -> str:
        return Path(pdf_path).stem