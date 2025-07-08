"""
Simple Medical Form Processor with Concurrent Processing

Load chunks, identify disjoint sections, fill JSON using concurrent calls.
Processes independent sections in parallel for improved performance.

Usage: python simple_form_processor.py
"""

import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import concurrent.futures

try:
    import vertexai
    from vertexai.generative_models import GenerativeModel, Part
    VERTEX_AVAILABLE = True
except ImportError:
    print("Warning: Vertex AI not available. Install with: pip install google-cloud-aiplatform")
    VERTEX_AVAILABLE = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not available. Set environment variables manually.")


class SimpleFormProcessor:
    """Form processor with concurrent processing for disjoint sections."""
    
    def __init__(self, project_id: str = "suki-dev", location: str = "us-central1", max_workers: int = 4):
        """Initialize the processor."""
        if not VERTEX_AVAILABLE:
            raise ImportError("Vertex AI is required. Install with: pip install google-cloud-aiplatform")
            
        vertexai.init(project=project_id, location=location)
        self.model = GenerativeModel("gemini-1.5-pro")
        self.max_workers = max_workers
        
    def set_max_workers(self, max_workers: int) -> None:
        """Set the maximum number of concurrent workers."""
        self.max_workers = max_workers
        print(f"Max workers set to: {max_workers}")
        
    def load_chunks(self, chunks_file: str) -> List[Dict[str, Any]]:
        """Load chunks from JSON file."""
        # Handle relative paths from src directory
        if not os.path.isabs(chunks_file):
            # If running from src/, go up one level
            if os.path.basename(os.getcwd()) == 'src':
                chunks_file = os.path.join('..', chunks_file)
        
        try:
            with open(chunks_file, "r") as f:
                chunks = json.load(f)
            print(f"Loaded {len(chunks)} chunks from {chunks_file}")
            return chunks
        except FileNotFoundError:
            print(f"ERROR: File not found: {chunks_file}")
            print(f"Current working directory: {os.getcwd()}")
            print(f"Looking for file at: {os.path.abspath(chunks_file)}")
            return []
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON: {e}")
            return []
    
    def load_image_bytes(self, image_path: str) -> Optional[bytes]:
        """Load image as bytes."""
        try:
            with open(image_path, "rb") as f:
                return f.read()
        except FileNotFoundError:
            print(f"Warning: Image not found: {image_path}")
            return None
    
    def find_disjoint_sections(self, chunks: List[Dict[str, Any]]) -> List[List[int]]:
        """
        Find disjoint (independent) sections in the form chunks.
        Returns groups of chunk indices that can be processed separately.
        """
        print(f"Analyzing {len(chunks)} chunks to identify disjoint sections...")
        
        try:
            # Build prompt
            prompt = """
            Analyze these medical form chunks and identify DISJOINT sections.
            
            Disjoint means each section contains completely independent information:
            - Patient Demographics (separate from everything else)
            - Medical History (independent from current visit)
            - Current Symptoms/Examination (separate from history)
            - Treatment Plan (independent from history)
            - Administrative Info (separate from medical content)
            
            The goal is to find sections that can be processed independently without 
            losing any relationships between fields.
            
            Return ONLY a JSON array of arrays with chunk indices.
            Example: [[0,1,2], [3,4], [5,6,7]]
            
            Chunks to analyze:
            """
            
            parts = [prompt]
            
            # Add chunks with limited text and images
            for i, chunk in enumerate(chunks):
                text = chunk.get('text', '')[:300]  # Limit text
                parts.append(f"\nChunk {i}: {text}")
                
                # Add first image if available
                if chunk.get('image_paths') and len(chunk['image_paths']) > 0:
                    image_path = chunk['image_paths'][0]
                    image_bytes = self.load_image_bytes(image_path)
                    if image_bytes:
                        parts.append(Part.from_data(mime_type="image/png", data=image_bytes))
            
            parts.append("\nReturn JSON array of disjoint section indices:")
            
            response = self.model.generate_content(parts)
            
            if not response or not response.text:
                print("WARNING: Empty response from model, using fallback sectioning")
                return [[i] for i in range(len(chunks))]
            
            # Parse response
            response_text = response.text.strip()
            if response_text.startswith("```"):
                lines = response_text.split('\n')
                response_text = '\n'.join(lines[1:-1])
            
            sections = json.loads(response_text)
            print(f"Identified {len(sections)} disjoint sections")
            
            # Print section breakdown
            for i, section in enumerate(sections):
                print(f"  Section {i}: chunks {section}")
            
            return sections
            
        except Exception as e:
            print(f"ERROR: Failed to identify sections: {e}")
            print("Using fallback: treating each chunk as separate section")
            return [[i] for i in range(len(chunks))]
    
    def create_json_model(self, chunks: List[Dict[str, Any]], section_indices: List[int]) -> Dict[str, Any]:
        """Create JSON structure for a section."""
        print(f"Creating JSON model for section: {section_indices}")
        
        try:
            # Combine text from section
            section_text = ""
            section_images = []
            
            for idx in section_indices:
                chunk = chunks[idx]
                section_text += f"\n{chunk.get('text', '')}\n"
                
                if chunk.get('image_paths'):
                    section_images.extend(chunk['image_paths'][:2])
            
            prompt = f"""
            Create a JSON structure for this medical form section.
            
            Look at the text and images to identify:
            - Field names (use clear, descriptive names)
            - Field types (string, number, boolean, array)
            - Required information vs optional
            
            Return a clean JSON object with the structure, like:
            {{
                "patient_name": "string",
                "date_of_birth": "string", 
                "medications": ["array of strings"],
                "has_allergies": "boolean"
            }}
            
            Section content:
            {section_text}
            
            Return ONLY the JSON structure:
            """
            
            parts = [prompt]
            
            # Add images
            for img_path in section_images[:2]:  # Max 2 images
                image_bytes = self.load_image_bytes(img_path)
                if image_bytes:
                    parts.append(Part.from_data(mime_type="image/png", data=image_bytes))
            
            response = self.model.generate_content(parts)
            
            if not response or not response.text:
                return {"error": "Empty response"}
            
            # Parse response
            response_text = response.text.strip()
            if response_text.startswith("```"):
                lines = response_text.split('\n')
                response_text = '\n'.join(lines[1:-1])
            
            # Fix incomplete JSON
            open_braces = response_text.count('{')
            close_braces = response_text.count('}')
            if open_braces > close_braces:
                response_text += '}' * (open_braces - close_braces)
            
            model = json.loads(response_text)
            print(f"Created model with {len(model)} fields")
            return model
            
        except Exception as e:
            print(f"ERROR: Failed to create model: {e}")
            return {"error": f"Model creation failed: {str(e)}"}
    
    def fill_json_data(self, json_model: Dict[str, Any], transcript: str, section_id: int) -> Dict[str, Any]:
        """Fill JSON model with patient data."""
        print(f"Filling data for section {section_id}")
        
        try:
            prompt = f"""
            Fill this JSON structure with data from the patient transcript.
            
            RULES:
            - Use ONLY information explicitly stated in the transcript
            - If information is not available, use null
            - Do not invent or guess any information
            - Keep the same field names and structure
            - Use appropriate data types (strings, numbers, booleans, arrays)
            
            JSON STRUCTURE TO FILL:
            {json.dumps(json_model, indent=2)}
            
            PATIENT TRANSCRIPT:
            {transcript}
            
            Return ONLY the filled JSON:
            """
            
            response = self.model.generate_content([prompt])
            
            if not response or not response.text:
                return {"error": "Empty response"}
            
            # Parse response
            response_text = response.text.strip()
            if response_text.startswith("```"):
                lines = response_text.split('\n')
                response_text = '\n'.join(lines[1:-1])
            
            # Fix incomplete JSON
            open_braces = response_text.count('{')
            close_braces = response_text.count('}')
            if open_braces > close_braces:
                response_text += '}' * (open_braces - close_braces)
            
            filled_data = json.loads(response_text)
            field_count = len([v for v in filled_data.values() if v is not None])
            print(f"Filled {field_count}/{len(filled_data)} fields")
            return filled_data
            
        except Exception as e:
            print(f"ERROR: Failed to fill data: {e}")
            return {"error": f"Data filling failed: {str(e)}"}
    
    def process_section(self, chunks: List[Dict[str, Any]], section_indices: List[int], 
                       transcript: str, section_id: int) -> Dict[str, Any]:
        """Process one section: create model and fill with data."""
        print(f"\n--- Processing Section {section_id} ---")
        
        # Step 1: Create JSON model
        json_model = self.create_json_model(chunks, section_indices)
        if "error" in json_model:
            return {
                "section_id": section_id,
                "chunk_indices": section_indices,
                "status": "failed",
                "error": json_model["error"]
            }
        
        # Step 2: Fill with data
        filled_data = self.fill_json_data(json_model, transcript, section_id)
        
        return {
            "section_id": section_id,
            "chunk_indices": section_indices,
            "status": "success" if "error" not in filled_data else "failed",
            "json_model": json_model,
            "filled_data": filled_data
        }
    
    def _process_sections_concurrently(self, chunks: List[Dict[str, Any]], sections: List[List[int]], 
                                      transcript: str) -> List[Dict[str, Any]]:
        """Process multiple sections concurrently using ThreadPoolExecutor."""
        if not sections:
            print("No sections to process")
            return []
        
        # For single section, process directly without threading overhead
        if len(sections) == 1:
            print("Single section detected, processing directly...")
            return [self.process_section(chunks, sections[0], transcript, 0)]
        
        # Use fewer workers if there are fewer sections
        actual_workers = min(self.max_workers, len(sections))
        print(f"Using {actual_workers} concurrent workers for {len(sections)} sections...")
        
        # Process sections concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=actual_workers) as executor:
            # Submit all tasks
            future_to_section = {
                executor.submit(self.process_section, chunks, section_indices, transcript, section_id): section_id 
                for section_id, section_indices in enumerate(sections)
            }
            
            # Collect results in order
            results = [None] * len(sections)
            completed_count = 0
            
            for future in concurrent.futures.as_completed(future_to_section):
                section_id = future_to_section[future]
                try:
                    result = future.result()
                    results[section_id] = result
                    completed_count += 1
                    print(f"✓ Section {section_id} completed ({completed_count}/{len(sections)})")
                except Exception as e:
                    print(f"✗ Section {section_id} failed: {e}")
                    results[section_id] = {
                        "section_id": section_id,
                        "chunk_indices": sections[section_id],
                        "status": "failed",
                        "error": f"Concurrent execution failed: {str(e)}"
                    }
                    completed_count += 1
        
        return results
    
    def process_form(self, chunks_file: str, transcript: str) -> Dict[str, Any]:
        """
        Complete form processing with concurrent section processing.
        
        Args:
            chunks_file: Path to chunks JSON file
            transcript: Patient transcript
            
        Returns:
            Processing results with concurrent processing statistics
        """
        print("Starting form processing...")
        print("=" * 50)
        
        start_time = datetime.now()
        
        # Step 1: Load chunks
        chunks = self.load_chunks(chunks_file)
        if not chunks:
            return {"error": "Failed to load chunks"}
        
        # Step 2: Find disjoint sections
        sections = self.find_disjoint_sections(chunks)
        
        # Step 3: Process each section concurrently
        print(f"\nProcessing {len(sections)} sections concurrently...")
        
        results = self._process_sections_concurrently(chunks, sections, transcript)
        
        # Step 4: Print results summary
        for i, result in enumerate(results):
            status = "SUCCESS" if result["status"] == "success" else "FAILED"
            print(f"Section {i}: {status}")
        
        # Step 5: Combine successful results
        final_form = {}
        successful_count = 0
        
        for result in results:
            if result["status"] == "success" and "filled_data" in result:
                if isinstance(result["filled_data"], dict) and "error" not in result["filled_data"]:
                    section_name = f"section_{result['section_id']}"
                    final_form[section_name] = result["filled_data"]
                    successful_count += 1
        
        # Step 6: Create summary
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        summary = {
            "timestamp": start_time.isoformat(),
            "processing_time_seconds": processing_time,
            "total_chunks": len(chunks),
            "total_sections": len(sections),
            "successful_sections": successful_count,
            "failed_sections": len(sections) - successful_count,
            "success_rate": successful_count / len(sections) if sections else 0
        }
        
        return {
            "summary": summary,
            "disjoint_sections": sections,
            "section_results": results,
            "final_form": final_form
        }
    
    def save_outputs(self, results: Dict[str, Any]) -> None:
        """Save output files."""
        os.makedirs("outputs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Main output: final form
        final_form_path = f"outputs/filled_form_{timestamp}.json"
        with open(final_form_path, "w") as f:
            json.dump(results["final_form"], f, indent=2)
        
        # Detailed results
        detailed_path = f"outputs/detailed_results_{timestamp}.json"
        with open(detailed_path, "w") as f:
            json.dump(results, f, indent=2)
        
        # Summary report
        report_path = f"outputs/processing_report_{timestamp}.txt"
        self.create_report(results, report_path)
        
        print(f"\nOutput files saved:")
        print(f"  Final Form: {final_form_path}")
        print(f"  Detailed Results: {detailed_path}")
        print(f"  Report: {report_path}")
    
    def create_report(self, results: Dict[str, Any], report_path: str) -> None:
        """Create human-readable report."""
        summary = results["summary"]
        
        report = f"""MEDICAL FORM PROCESSING REPORT
Generated: {summary["timestamp"]}
Processing Time: {summary["processing_time_seconds"]:.2f} seconds

SUMMARY
=======
Total Chunks: {summary["total_chunks"]}
Disjoint Sections: {summary["total_sections"]}
Successful Sections: {summary["successful_sections"]}
Failed Sections: {summary["failed_sections"]}
Success Rate: {summary["success_rate"]:.1%}

SECTION BREAKDOWN
================
"""
        
        for result in results["section_results"]:
            section_id = result["section_id"]
            status = result["status"]
            chunks = result.get("chunk_indices", [])
            
            report += f"Section {section_id}: {status.upper()} (chunks: {chunks})\n"
            
            if status == "success" and "filled_data" in result:
                data = result["filled_data"]
                if isinstance(data, dict):
                    filled_fields = len([v for v in data.values() if v is not None])
                    total_fields = len(data)
                    report += f"  Filled: {filled_fields}/{total_fields} fields\n"
            elif status == "failed":
                report += f"  Error: {result.get('error', 'Unknown error')}\n"
        
        report += f"""
FINAL FORM
==========
Sections in final form: {len(results["final_form"])}
"""
        
        for section_name, section_data in results["final_form"].items():
            if isinstance(section_data, dict):
                field_count = len(section_data)
                report += f"  {section_name}: {field_count} fields\n"
        
        with open(report_path, "w") as f:
            f.write(report)


def get_sample_transcript() -> str:
    """Sample patient transcript."""
    return """
    Patient: Robert Chen, DOB: 02/08/1968
    Address: 842 Elm Street, Kansas City, Missouri 64111
    Phone: 816-555-3421
    Medicare: 123-45-6789A
    Height: 70 inches, Weight: 185 lbs, Sex: Male

    Doctor: Dr. Maria Rodriguez, Sleep Medicine
    NPI: 1234567890
    Phone: 816-555-7890

    Patient: Doctor, I'm here about my sleep study results. My wife says I stop breathing at night and I'm exhausted all the time.

    Doctor: Yes Mr. Chen, your sleep study from December 18th, 2024 shows severe obstructive sleep apnea. Your AHI is 42 events per hour. You also have hypertension which qualifies you for CPAP treatment.

    Patient: What does that mean for treatment?

    Doctor: I'm prescribing a CPAP machine, HCPCS code E0601, with humidifier E0562. This is for obstructive sleep apnea, diagnosis code 327.23. You'll need this for life - 99 months in medical terms.

    Patient: Will insurance cover it?

    Doctor: Yes, Medicare covers it. Today January 15th, 2025 is your initial face-to-face evaluation. Your sleep test was conducted at our facility-based lab. You need to use it 4+ hours per night, 70% of nights over 30 days.

    Patient: What if CPAP doesn't work?

    Doctor: We can try BiPAP if CPAP is ineffective, but we start with CPAP first. I'm referring you to MedEquip Solutions, NPI 9876543210, for home delivery.

    Patient: When do I follow up?

    Doctor: March 1st, 2025 to check your compliance and see if symptoms improved. The machine tracks your usage automatically.
    """


def main():
    """Main function."""
    if not VERTEX_AVAILABLE:
        print("Error: Vertex AI not available. Install with: pip install google-cloud-aiplatform")
        return
    
    # Configuration
    chunks_file = "archived_outputs/outputs_2/chunks.json"
    transcript = get_sample_transcript()
    
    print("CONCURRENT MEDICAL FORM PROCESSOR")
    print("=" * 50)
    print(f"Chunks file: {chunks_file}")
    print("=" * 50)
    
    # Initialize and run
    try:
        processor = SimpleFormProcessor(max_workers=4)  # Use 4 concurrent workers
        results = processor.process_form(chunks_file, transcript)
        
        if "error" in results:
            print(f"ERROR: Processing failed: {results['error']}")
            return
        
        # Save outputs
        processor.save_outputs(results)
        
        # Print summary
        summary = results["summary"]
        print("\nPROCESSING COMPLETE!")
        print("=" * 50)
        print(f"Processing time: {summary['processing_time_seconds']:.1f}s")
        print(f"Success rate: {summary['successful_sections']}/{summary['total_sections']} sections")
        print(f"Final form sections: {len(results['final_form'])}")
        
    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    main()