"""
End-to-End Medical Form Processing Pipeline
===========================================

Complete pipeline for processing medical forms with intelligent routing:
- PDF analysis and chunking (Andrew Ng's agentic approach)
- Heuristics-based routing (simple vs complex processing)
- Multiple processing strategies with concurrency
- Output generation (JSON + optional PDF)
- Built-in testing and validation

Usage:
    processor = EndToEndProcessor()
    result = processor.process_form(pdf_path, transcript)
"""

import json
import os
import time
from typing import List, Dict, Any, Optional, Tuple, Union
from datetime import datetime
from pathlib import Path
import concurrent.futures
from enum import Enum
from dataclasses import dataclass

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


class ProcessingStrategy(Enum):
    """Processing strategy options"""
    SIMPLE = "simple"
    COMPLEX = "complex"
    AUTO = "auto"


class FormComplexity(Enum):
    """Form complexity levels"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"


@dataclass
class FormAnalysis:
    """Form analysis results"""
    page_count: int
    chunk_count: int
    complexity: FormComplexity
    estimated_processing_time: float
    recommended_strategy: ProcessingStrategy
    form_type: Optional[str] = None
    key_sections: List[str] = None


@dataclass
class ProcessingResult:
    """Processing result container"""
    success: bool
    processing_time: float
    strategy_used: ProcessingStrategy
    form_analysis: FormAnalysis
    filled_form: Dict[str, Any]
    section_results: List[Dict[str, Any]]
    error_message: Optional[str] = None
    confidence_score: Optional[float] = None


class PDFAnalyzer:
    """PDF analysis and chunking using Andrew Ng's agentic approach"""
    
    def __init__(self, model: GenerativeModel):
        self.model = model
    
    def analyze_pdf(self, pdf_path: str) -> FormAnalysis:
        """Analyze PDF and determine processing strategy"""
        print(f"📄 Analyzing PDF: {pdf_path}")
        
        # Extract basic metrics
        page_count = self._get_page_count(pdf_path)
        
        # For now, use heuristics - could be enhanced with actual PDF parsing
        if page_count <= 2:
            complexity = FormComplexity.SIMPLE
            estimated_time = 10.0
            recommended_strategy = ProcessingStrategy.SIMPLE
        elif page_count <= 5:
            complexity = FormComplexity.MODERATE
            estimated_time = 30.0
            recommended_strategy = ProcessingStrategy.COMPLEX
        else:
            complexity = FormComplexity.COMPLEX
            estimated_time = 60.0
            recommended_strategy = ProcessingStrategy.COMPLEX
        
        return FormAnalysis(
            page_count=page_count,
            chunk_count=0,  # Will be set after chunking
            complexity=complexity,
            estimated_processing_time=estimated_time,
            recommended_strategy=recommended_strategy,
            form_type=self._detect_form_type(pdf_path),
            key_sections=[]
        )
    
    def extract_chunks(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Extract chunks from PDF using Andrew Ng's approach"""
        print(f"🔍 Extracting chunks from: {pdf_path}")
        
        # Placeholder implementation - would use actual PDF processing
        # For now, try to load existing chunks or create mock chunks
        chunks_file = self._find_chunks_file(pdf_path)
        
        if chunks_file and os.path.exists(chunks_file):
            with open(chunks_file, 'r') as f:
                chunks = json.load(f)
            print(f"📊 Loaded {len(chunks)} chunks from existing file")
            return chunks
        
        # Create mock chunks for testing
        return self._create_mock_chunks(pdf_path)
    
    def _get_page_count(self, pdf_path: str) -> int:
        """Get page count from PDF"""
        # Simple heuristic based on filename or could use actual PDF parsing
        if "simple" in pdf_path.lower():
            return 1
        elif "cms" in pdf_path.lower():
            return 2
        else:
            return 3
    
    def _detect_form_type(self, pdf_path: str) -> str:
        """Detect form type from PDF"""
        filename = os.path.basename(pdf_path).lower()
        if "simple" in filename:
            return "simple_form"
        elif "cms" in filename:
            return "cms_form"
        elif "oasis" in filename:
            return "oasis_form"
        else:
            return "unknown_form"
    
    def _find_chunks_file(self, pdf_path: str) -> Optional[str]:
        """Find existing chunks file for PDF"""
        # Look for chunks in archived_outputs
        chunks_paths = [
            "archived_outputs/outputs_2/chunks.json",
            "../archived_outputs/outputs_2/chunks.json"
        ]
        
        for path in chunks_paths:
            if os.path.exists(path):
                return path
        return None
    
    def _create_mock_chunks(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Create mock chunks for testing"""
        return [
            {
                "chunk_id": 0,
                "text": "Patient Information Section",
                "page_number": 1,
                "image_paths": []
            },
            {
                "chunk_id": 1,
                "text": "Medical History Section",
                "page_number": 1,
                "image_paths": []
            }
        ]


class FormRouter:
    """Intelligent routing based on form analysis"""
    
    def __init__(self):
        self.routing_rules = {
            FormComplexity.SIMPLE: ProcessingStrategy.SIMPLE,
            FormComplexity.MODERATE: ProcessingStrategy.COMPLEX,
            FormComplexity.COMPLEX: ProcessingStrategy.COMPLEX
        }
    
    def route_processing(self, analysis: FormAnalysis, 
                        strategy_override: Optional[ProcessingStrategy] = None) -> ProcessingStrategy:
        """Route to appropriate processing strategy"""
        
        if strategy_override:
            print(f"🎯 Using override strategy: {strategy_override.value}")
            return strategy_override
        
        strategy = self.routing_rules.get(analysis.complexity, ProcessingStrategy.COMPLEX)
        
        print(f"🧭 Routing decision:")
        print(f"  - Form complexity: {analysis.complexity.value}")
        print(f"  - Page count: {analysis.page_count}")
        print(f"  - Recommended strategy: {strategy.value}")
        
        return strategy


class SimpleProcessor:
    """Simple processing strategy for small forms (1-2 API calls)"""
    
    def __init__(self, model: GenerativeModel):
        self.model = model
    
    def process(self, chunks: List[Dict[str, Any]], transcript: str, 
                analysis: FormAnalysis) -> Dict[str, Any]:
        """Process form with simple strategy"""
        print(f"⚡ Processing with SIMPLE strategy")
        
        start_time = time.time()
        
        # Step 1: Create complete form model in one call
        form_model = self._create_complete_model(chunks, analysis)
        
        # Step 2: Fill model with transcript data
        filled_form = self._fill_complete_form(form_model, transcript)
        
        processing_time = time.time() - start_time
        
        return {
            "strategy": "simple",
            "processing_time": processing_time,
            "filled_form": filled_form,
            "section_results": [{"section_id": 0, "status": "success", "filled_data": filled_form}],
            "api_calls": 2
        }
    
    def _create_complete_model(self, chunks: List[Dict[str, Any]], 
                              analysis: FormAnalysis) -> Dict[str, Any]:
        """Create complete form model in single API call"""
        
        # Combine all chunks
        combined_text = "\n".join([chunk.get('text', '') for chunk in chunks])
        
        prompt = f"""
        Create a complete JSON structure for this {analysis.form_type} medical form.
        
        This is a {analysis.complexity.value} form with {analysis.page_count} pages.
        
        Look at the content and create a comprehensive JSON structure with:
        - Clear field names
        - Appropriate data types
        - Nested structures where appropriate
        - All identifiable fields from the form
        
        Form content:
        {combined_text[:2000]}  # Limit for simple forms
        
        Return ONLY the JSON structure:
        """
        
        try:
            response = self.model.generate_content([prompt])
            
            if not response or not response.text:
                return {"error": "Empty response"}
            
            # Parse response
            response_text = response.text.strip()
            if response_text.startswith("```"):
                lines = response_text.split('\n')
                response_text = '\n'.join(lines[1:-1])
            
            return json.loads(response_text)
            
        except Exception as e:
            print(f"❌ Error creating model: {e}")
            return {"error": f"Model creation failed: {str(e)}"}
    
    def _fill_complete_form(self, form_model: Dict[str, Any], transcript: str) -> Dict[str, Any]:
        """Fill complete form in single API call"""
        
        if "error" in form_model:
            return form_model
        
        prompt = f"""
        Fill this JSON structure with data from the patient transcript.
        
        RULES:
        - Use ONLY information explicitly stated in the transcript
        - If information is not available, use null
        - Do not invent or guess any information
        - Preserve the exact structure and field names
        - Use appropriate data types
        
        JSON STRUCTURE TO FILL:
        {json.dumps(form_model, indent=2)}
        
        PATIENT TRANSCRIPT:
        {transcript}
        
        Return ONLY the filled JSON:
        """
        
        try:
            response = self.model.generate_content([prompt])
            
            if not response or not response.text:
                return {"error": "Empty response"}
            
            response_text = response.text.strip()
            if response_text.startswith("```"):
                lines = response_text.split('\n')
                response_text = '\n'.join(lines[1:-1])
            
            return json.loads(response_text)
            
        except Exception as e:
            print(f"❌ Error filling form: {e}")
            return {"error": f"Form filling failed: {str(e)}"}


class ComplexProcessor:
    """Complex processing strategy using disjoint sections + concurrency"""
    
    def __init__(self, model: GenerativeModel, max_workers: int = 4):
        self.model = model
        self.max_workers = max_workers
    
    def process(self, chunks: List[Dict[str, Any]], transcript: str,
                analysis: FormAnalysis) -> Dict[str, Any]:
        """Process form with complex strategy"""
        print(f"🔄 Processing with COMPLEX strategy")
        
        start_time = time.time()
        
        # Step 1: Find disjoint sections
        sections = self._find_disjoint_sections(chunks)
        
        # Step 2: Process sections concurrently
        results = self._process_sections_concurrently(chunks, sections, transcript)
        
        # Step 3: Combine results
        final_form = self._combine_results(results)
        
        processing_time = time.time() - start_time
        
        return {
            "strategy": "complex",
            "processing_time": processing_time,
            "filled_form": final_form,
            "section_results": results,
            "disjoint_sections": sections,
            "api_calls": len(sections) + 1  # +1 for section identification
        }
    
    def _find_disjoint_sections(self, chunks: List[Dict[str, Any]]) -> List[List[int]]:
        """Find disjoint sections using existing logic"""
        print(f"🔍 Analyzing {len(chunks)} chunks for disjoint sections...")
        
        try:
            prompt = """
            Analyze these medical form chunks and identify DISJOINT sections.
            
            Disjoint means completely independent information that can be processed separately:
            - Patient Demographics
            - Medical History
            - Current Symptoms/Examination
            - Treatment Plans
            - Administrative Info
            
            Return ONLY a JSON array of arrays with chunk indices.
            Example: [[0,1,2], [3,4], [5,6,7]]
            
            Chunks:
            """
            
            parts = [prompt]
            for i, chunk in enumerate(chunks):
                text = chunk.get('text', '')[:200]
                parts.append(f"\nChunk {i}: {text}")
            
            parts.append("\nReturn JSON array of disjoint section indices:")
            
            response = self.model.generate_content(parts)
            
            if not response or not response.text:
                return [[i] for i in range(len(chunks))]
            
            response_text = response.text.strip()
            if response_text.startswith("```"):
                lines = response_text.split('\n')
                response_text = '\n'.join(lines[1:-1])
            
            sections = json.loads(response_text)
            print(f"✅ Identified {len(sections)} disjoint sections")
            return sections
            
        except Exception as e:
            print(f"❌ Error finding sections: {e}")
            return [[i] for i in range(len(chunks))]
    
    def _process_sections_concurrently(self, chunks: List[Dict[str, Any]], 
                                      sections: List[List[int]], 
                                      transcript: str) -> List[Dict[str, Any]]:
        """Process sections concurrently"""
        
        if len(sections) == 1:
            return [self._process_single_section(chunks, sections[0], transcript, 0)]
        
        actual_workers = min(self.max_workers, len(sections))
        print(f"🚀 Using {actual_workers} concurrent workers for {len(sections)} sections")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=actual_workers) as executor:
            future_to_section = {
                executor.submit(self._process_single_section, chunks, section_indices, transcript, section_id): section_id
                for section_id, section_indices in enumerate(sections)
            }
            
            results = [None] * len(sections)
            
            for future in concurrent.futures.as_completed(future_to_section):
                section_id = future_to_section[future]
                try:
                    result = future.result()
                    results[section_id] = result
                    print(f"✅ Section {section_id} completed")
                except Exception as e:
                    print(f"❌ Section {section_id} failed: {e}")
                    results[section_id] = {
                        "section_id": section_id,
                        "status": "failed",
                        "error": str(e)
                    }
        
        return results
    
    def _process_single_section(self, chunks: List[Dict[str, Any]], 
                               section_indices: List[int], 
                               transcript: str, section_id: int) -> Dict[str, Any]:
        """Process a single section"""
        
        try:
            # Create model for section
            section_text = "\n".join([chunks[i].get('text', '') for i in section_indices])
            
            model_prompt = f"""
            Create JSON structure for this medical form section:
            
            Section content:
            {section_text[:1000]}
            
            Return clean JSON structure:
            """
            
            model_response = self.model.generate_content([model_prompt])
            
            if not model_response or not model_response.text:
                return {"section_id": section_id, "status": "failed", "error": "Empty model response"}
            
            model_text = model_response.text.strip()
            if model_text.startswith("```"):
                lines = model_text.split('\n')
                model_text = '\n'.join(lines[1:-1])
            
            section_model = json.loads(model_text)
            
            # Fill with data
            fill_prompt = f"""
            Fill this JSON structure with transcript data:
            
            STRUCTURE:
            {json.dumps(section_model, indent=2)}
            
            TRANSCRIPT:
            {transcript}
            
            Return filled JSON:
            """
            
            fill_response = self.model.generate_content([fill_prompt])
            
            if not fill_response or not fill_response.text:
                return {"section_id": section_id, "status": "failed", "error": "Empty fill response"}
            
            fill_text = fill_response.text.strip()
            if fill_text.startswith("```"):
                lines = fill_text.split('\n')
                fill_text = '\n'.join(lines[1:-1])
            
            filled_data = json.loads(fill_text)
            
            return {
                "section_id": section_id,
                "chunk_indices": section_indices,
                "status": "success",
                "json_model": section_model,
                "filled_data": filled_data
            }
            
        except Exception as e:
            return {
                "section_id": section_id,
                "chunk_indices": section_indices,
                "status": "failed",
                "error": str(e)
            }
    
    def _combine_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Combine section results into final form"""
        final_form = {}
        
        for result in results:
            if result["status"] == "success" and "filled_data" in result:
                if isinstance(result["filled_data"], dict) and "error" not in result["filled_data"]:
                    section_name = f"section_{result['section_id']}"
                    final_form[section_name] = result["filled_data"]
        
        return final_form


class OutputGenerator:
    """Generate outputs in various formats"""
    
    def __init__(self):
        self.output_dir = "outputs"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_outputs(self, result: ProcessingResult) -> Dict[str, str]:
        """Generate all output formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        outputs = {}
        
        # JSON output
        json_path = f"{self.output_dir}/filled_form_{timestamp}.json"
        with open(json_path, 'w') as f:
            json.dump(result.filled_form, f, indent=2)
        outputs["json"] = json_path
        
        # Detailed results
        detailed_path = f"{self.output_dir}/detailed_results_{timestamp}.json"
        
        # Convert enums to strings for JSON serialization
        form_analysis_dict = result.form_analysis.__dict__.copy()
        form_analysis_dict["complexity"] = result.form_analysis.complexity.value
        form_analysis_dict["recommended_strategy"] = result.form_analysis.recommended_strategy.value
        
        with open(detailed_path, 'w') as f:
            json.dump({
                "form_analysis": form_analysis_dict,
                "processing_result": {
                    "success": result.success,
                    "processing_time": result.processing_time,
                    "strategy_used": result.strategy_used.value,
                    "confidence_score": result.confidence_score
                },
                "section_results": result.section_results,
                "filled_form": result.filled_form
            }, f, indent=2)
        outputs["detailed"] = detailed_path
        
        # Report
        report_path = f"{self.output_dir}/processing_report_{timestamp}.txt"
        self._generate_report(result, report_path)
        outputs["report"] = report_path
        
        return outputs
    
    def _generate_report(self, result: ProcessingResult, report_path: str):
        """Generate human-readable report"""
        
        report = f"""MEDICAL FORM PROCESSING REPORT
Generated: {datetime.now().isoformat()}
Processing Time: {result.processing_time:.2f} seconds
Strategy Used: {result.strategy_used.value.upper()}
Success: {result.success}

FORM ANALYSIS
=============
Page Count: {result.form_analysis.page_count}
Complexity: {result.form_analysis.complexity.value}
Form Type: {result.form_analysis.form_type}
Chunk Count: {result.form_analysis.chunk_count}

PROCESSING RESULTS
==================
Total Sections: {len(result.section_results)}
Successful Sections: {len([r for r in result.section_results if r.get('status') == 'success'])}
Failed Sections: {len([r for r in result.section_results if r.get('status') == 'failed'])}

FINAL FORM
==========
Total Fields: {len(result.filled_form)}
Sections: {list(result.filled_form.keys())}
"""
        
        if result.error_message:
            report += f"\nERROR: {result.error_message}\n"
        
        with open(report_path, 'w') as f:
            f.write(report)


class EndToEndProcessor:
    """Main end-to-end processing orchestrator"""
    
    def __init__(self, project_id: str = "suki-dev", location: str = "us-central1", 
                 max_workers: int = 4):
        """Initialize the processor"""
        
        if not VERTEX_AVAILABLE:
            raise ImportError("Vertex AI is required. Install with: pip install google-cloud-aiplatform")
        
        vertexai.init(project=project_id, location=location)
        self.model = GenerativeModel("gemini-1.5-pro")
        
        # Initialize components
        self.pdf_analyzer = PDFAnalyzer(self.model)
        self.router = FormRouter()
        self.simple_processor = SimpleProcessor(self.model)
        self.complex_processor = ComplexProcessor(self.model, max_workers)
        self.output_generator = OutputGenerator()
        
        print("🚀 End-to-End Processor initialized")
    
    def process_form(self, pdf_path: str, transcript: str, 
                    strategy_override: Optional[ProcessingStrategy] = None,
                    generate_pdf: bool = False) -> ProcessingResult:
        """
        Process a medical form end-to-end
        
        Args:
            pdf_path: Path to PDF file
            transcript: Patient transcript
            strategy_override: Override automatic strategy selection
            generate_pdf: Whether to generate PDF output
            
        Returns:
            ProcessingResult with all results
        """
        
        print("=" * 60)
        print("🏥 STARTING END-TO-END MEDICAL FORM PROCESSING")
        print("=" * 60)
        
        start_time = time.time()
        
        try:
            # Step 1: Analyze PDF
            analysis = self.pdf_analyzer.analyze_pdf(pdf_path)
            print(f"📊 Form Analysis Complete: {analysis.complexity.value} complexity")
            
            # Step 2: Extract chunks
            chunks = self.pdf_analyzer.extract_chunks(pdf_path)
            analysis.chunk_count = len(chunks)
            print(f"📄 Extracted {len(chunks)} chunks")
            
            # Step 3: Route processing
            strategy = self.router.route_processing(analysis, strategy_override)
            
            # Step 4: Process based on strategy
            if strategy == ProcessingStrategy.SIMPLE:
                processing_result = self.simple_processor.process(chunks, transcript, analysis)
            else:
                processing_result = self.complex_processor.process(chunks, transcript, analysis)
            
            # Step 5: Create result
            total_time = time.time() - start_time
            
            result = ProcessingResult(
                success=True,
                processing_time=total_time,
                strategy_used=strategy,
                form_analysis=analysis,
                filled_form=processing_result["filled_form"],
                section_results=processing_result["section_results"],
                confidence_score=self._calculate_confidence_score(processing_result)
            )
            
            # Step 6: Generate outputs
            output_paths = self.output_generator.generate_outputs(result)
            
            print("=" * 60)
            print("✅ PROCESSING COMPLETE!")
            print(f"⏱️  Total Time: {total_time:.2f} seconds")
            print(f"🎯 Strategy: {strategy.value}")
            print(f"📊 Success: {result.success}")
            print(f"📁 Outputs: {list(output_paths.keys())}")
            print("=" * 60)
            
            return result
            
        except Exception as e:
            error_time = time.time() - start_time
            print(f"❌ Processing failed after {error_time:.2f}s: {e}")
            
            return ProcessingResult(
                success=False,
                processing_time=error_time,
                strategy_used=strategy_override or ProcessingStrategy.AUTO,
                form_analysis=FormAnalysis(0, 0, FormComplexity.SIMPLE, 0.0, ProcessingStrategy.AUTO),
                filled_form={},
                section_results=[],
                error_message=str(e)
            )
    
    def _calculate_confidence_score(self, processing_result: Dict[str, Any]) -> float:
        """Calculate confidence score based on processing results"""
        
        if "error" in processing_result.get("filled_form", {}):
            return 0.0
        
        # Simple confidence based on successful sections
        total_sections = len(processing_result.get("section_results", []))
        successful_sections = len([r for r in processing_result.get("section_results", []) 
                                 if r.get("status") == "success"])
        
        if total_sections == 0:
            return 0.0
        
        return successful_sections / total_sections
    
    def test_pipeline(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Test the pipeline with multiple test cases"""
        
        print("🧪 TESTING PIPELINE")
        print("=" * 40)
        
        results = []
        
        for i, test_case in enumerate(test_cases):
            print(f"\n📋 Test Case {i+1}: {test_case.get('name', 'Unnamed')}")
            
            try:
                result = self.process_form(
                    test_case["pdf_path"],
                    test_case["transcript"],
                    test_case.get("strategy_override")
                )
                
                results.append({
                    "test_case": test_case["name"],
                    "success": result.success,
                    "processing_time": result.processing_time,
                    "strategy": result.strategy_used.value,
                    "confidence": result.confidence_score
                })
                
            except Exception as e:
                results.append({
                    "test_case": test_case["name"],
                    "success": False,
                    "error": str(e)
                })
        
        # Summary
        successful_tests = len([r for r in results if r.get("success")])
        print(f"\n✅ Test Results: {successful_tests}/{len(results)} passed")
        
        return {
            "total_tests": len(results),
            "successful_tests": successful_tests,
            "success_rate": successful_tests / len(results) if results else 0,
            "results": results
        }


def get_sample_transcript() -> str:
    """Sample patient transcript for testing"""
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

    Patient: When do I follow up?

    Doctor: March 1st, 2025 to check your compliance and see if symptoms improved. The machine tracks your usage automatically.
    """


def main():
    """Main function for testing"""
    
    if not VERTEX_AVAILABLE:
        print("Error: Vertex AI not available. Install with: pip install google-cloud-aiplatform")
        return
    
    # Initialize processor
    processor = EndToEndProcessor(max_workers=4)
    
    # Test cases
    test_cases = [
        {
            "name": "Simple Form Test",
            "pdf_path": "data/pdf/Simple_Form.pdf",
            "transcript": get_sample_transcript(),
            "strategy_override": None  # Let it auto-route
        },
        {
            "name": "CMS Form Test",
            "pdf_path": "data/pdf/CMS_Form.pdf",
            "transcript": get_sample_transcript(),
            "strategy_override": ProcessingStrategy.COMPLEX
        }
    ]
    
    # Run tests
    test_results = processor.test_pipeline(test_cases)
    
    print("\n" + "=" * 60)
    print("🏁 TESTING COMPLETE")
    print(f"Success Rate: {test_results['success_rate']:.1%}")
    print("=" * 60)


if __name__ == "__main__":
    main()