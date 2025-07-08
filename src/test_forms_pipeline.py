"""
Form-Specific Pipeline Testing
==============================

Test the end-to-end pipeline with form-specific transcripts to ensure
each form type is processed correctly with appropriate routing and results.

Usage:
    python test_forms_pipeline.py
"""

import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Any

# Add current directory to path for imports
sys.path.append('.')

from form_transcripts import FORM_TRANSCRIPTS, FORM_TEST_CASES, get_transcript_for_form
from end_to_end_processor import EndToEndProcessor, ProcessingStrategy, FormComplexity


class FormsPipelineTester:
    """Test the pipeline with different form types"""
    
    def __init__(self, run_api_tests: bool = False):
        """
        Initialize tester
        
        Args:
            run_api_tests: Whether to run tests that make actual API calls
        """
        self.run_api_tests = run_api_tests
        self.test_results = []
        
        if run_api_tests:
            try:
                self.processor = EndToEndProcessor(max_workers=2)
                print("✅ End-to-end processor initialized for API testing")
            except Exception as e:
                print(f"❌ Failed to initialize processor: {e}")
                self.processor = None
        else:
            self.processor = None
            print("🔍 Running non-API tests only")
    
    def test_transcript_quality(self) -> Dict[str, Any]:
        """Test the quality and coverage of each transcript"""
        print("\n📝 TESTING TRANSCRIPT QUALITY")
        print("=" * 40)
        
        results = {}
        
        for form_type, transcript in FORM_TRANSCRIPTS.items():
            print(f"\n🔍 Testing {form_type}...")
            
            # Basic quality checks
            word_count = len(transcript.split())
            line_count = len(transcript.strip().split('\n'))
            has_provider = any(role in transcript.lower() for role in ['nurse', 'doctor', 'physician', 'assistant'])
            has_patient = 'patient' in transcript.lower()
            has_dialogue = ':' in transcript
            
            # Content coverage
            test_case = next((tc for tc in FORM_TEST_CASES if tc['form_type'] == form_type), {})
            key_fields = test_case.get('key_fields', [])
            
            field_coverage = {}
            for field in key_fields:
                covered = field.lower() in transcript.lower()
                field_coverage[field] = covered
            
            coverage_rate = sum(field_coverage.values()) / len(field_coverage) if field_coverage else 0
            
            quality_score = sum([
                word_count >= 100,  # Reasonable length
                has_provider,       # Healthcare provider present
                has_patient,        # Patient present
                has_dialogue,       # Conversational format
                coverage_rate >= 0.75  # Good field coverage
            ]) / 5
            
            results[form_type] = {
                "word_count": word_count,
                "line_count": line_count,
                "has_provider": has_provider,
                "has_patient": has_patient,
                "has_dialogue": has_dialogue,
                "field_coverage": field_coverage,
                "coverage_rate": coverage_rate,
                "quality_score": quality_score,
                "passed": quality_score >= 0.8
            }
            
            status = "✅" if results[form_type]["passed"] else "❌"
            print(f"  {status} Quality Score: {quality_score:.1%}")
            print(f"    Words: {word_count}, Coverage: {coverage_rate:.1%}")
        
        return results
    
    def test_routing_logic(self) -> Dict[str, Any]:
        """Test that forms are routed to appropriate processing strategies"""
        print("\n🧭 TESTING ROUTING LOGIC")
        print("=" * 40)
        
        # Mock processor for routing tests
        from end_to_end_processor import FormRouter, FormAnalysis
        
        router = FormRouter()
        results = {}
        
        complexity_mapping = {
            "simple": FormComplexity.SIMPLE,
            "moderate": FormComplexity.MODERATE, 
            "complex": FormComplexity.COMPLEX
        }
        
        for test_case in FORM_TEST_CASES:
            form_type = test_case["form_type"]
            expected_complexity = test_case["expected_complexity"]
            
            print(f"\n🔍 Testing {form_type}...")
            
            # Create mock analysis
            complexity = complexity_mapping.get(expected_complexity, FormComplexity.MODERATE)
            
            analysis = FormAnalysis(
                page_count=1 if expected_complexity == "simple" else 3,
                chunk_count=2 if expected_complexity == "simple" else 8,
                complexity=complexity,
                estimated_processing_time=10.0 if expected_complexity == "simple" else 30.0,
                recommended_strategy=ProcessingStrategy.SIMPLE if expected_complexity == "simple" else ProcessingStrategy.COMPLEX,
                form_type=form_type
            )
            
            # Test routing
            strategy = router.route_processing(analysis)
            
            expected_strategy = ProcessingStrategy.SIMPLE if expected_complexity == "simple" else ProcessingStrategy.COMPLEX
            correct_routing = strategy == expected_strategy
            
            results[form_type] = {
                "expected_complexity": expected_complexity,
                "actual_strategy": strategy.value,
                "expected_strategy": expected_strategy.value,
                "correct_routing": correct_routing
            }
            
            status = "✅" if correct_routing else "❌"
            print(f"  {status} {expected_complexity} → {strategy.value}")
        
        return results
    
    def test_form_compatibility(self) -> Dict[str, Any]:
        """Test form compatibility with pipeline components"""
        print("\n⚙️ TESTING FORM COMPATIBILITY")
        print("=" * 40)
        
        results = {}
        
        for form_type in FORM_TRANSCRIPTS.keys():
            print(f"\n🔍 Testing {form_type}...")
            
            try:
                transcript = get_transcript_for_form(form_type)
                
                # Test transcript retrieval
                transcript_valid = len(transcript) > 50
                
                # Test JSON serialization compatibility
                import json
                test_data = {
                    "form_type": form_type,
                    "transcript_length": len(transcript),
                    "timestamp": datetime.now().isoformat()
                }
                json_serializable = True
                try:
                    json.dumps(test_data)
                except:
                    json_serializable = False
                
                # Test file path compatibility
                test_case = next((tc for tc in FORM_TEST_CASES if tc['form_type'] == form_type), {})
                pdf_path = test_case.get('pdf_path', '')
                path_valid = len(pdf_path) > 0
                
                compatibility_score = sum([
                    transcript_valid,
                    json_serializable,
                    path_valid
                ]) / 3
                
                results[form_type] = {
                    "transcript_valid": transcript_valid,
                    "json_serializable": json_serializable,
                    "path_valid": path_valid,
                    "compatibility_score": compatibility_score,
                    "passed": compatibility_score >= 0.8
                }
                
                status = "✅" if results[form_type]["passed"] else "❌"
                print(f"  {status} Compatibility: {compatibility_score:.1%}")
                
            except Exception as e:
                results[form_type] = {
                    "passed": False,
                    "error": str(e)
                }
                print(f"  ❌ Error: {e}")
        
        return results
    
    def test_end_to_end_processing(self) -> Dict[str, Any]:
        """Test end-to-end processing if API testing is enabled"""
        if not self.run_api_tests or not self.processor:
            print("\n⏭️  SKIPPING END-TO-END API TESTS (not enabled)")
            return {"skipped": True, "reason": "API testing not enabled"}
        
        print("\n🚀 TESTING END-TO-END PROCESSING")
        print("=" * 40)
        
        results = {}
        
        # Test with a simple form that shouldn't require actual API calls
        test_form = "simple_form"
        transcript = FORM_TRANSCRIPTS[test_form]
        
        try:
            print(f"\n🔍 Testing {test_form} end-to-end...")
            
            start_time = time.time()
            
            # This would normally make API calls - for testing, we'll simulate
            result = self.processor.process_form(
                "test_data/mock_simple_form.pdf",
                transcript,
                strategy_override=ProcessingStrategy.SIMPLE
            )
            
            processing_time = time.time() - start_time
            
            results[test_form] = {
                "success": result.success,
                "processing_time": processing_time,
                "strategy_used": result.strategy_used.value,
                "has_filled_form": len(result.filled_form) > 0,
                "confidence_score": result.confidence_score
            }
            
            status = "✅" if result.success else "❌"
            print(f"  {status} Processing: {processing_time:.2f}s")
            
        except Exception as e:
            results[test_form] = {
                "success": False,
                "error": str(e)
            }
            print(f"  ❌ Error: {e}")
        
        return results
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and return comprehensive results"""
        print("🧪 STARTING COMPREHENSIVE FORM PIPELINE TESTING")
        print("=" * 60)
        
        start_time = time.time()
        
        # Run all test suites
        transcript_results = self.test_transcript_quality()
        routing_results = self.test_routing_logic()
        compatibility_results = self.test_form_compatibility()
        e2e_results = self.test_end_to_end_processing()
        
        total_time = time.time() - start_time
        
        # Calculate overall results
        all_tests = []
        
        # Transcript quality
        for form_type, result in transcript_results.items():
            all_tests.append(result.get("passed", False))
        
        # Routing logic
        for form_type, result in routing_results.items():
            all_tests.append(result.get("correct_routing", False))
        
        # Compatibility
        for form_type, result in compatibility_results.items():
            all_tests.append(result.get("passed", False))
        
        # E2E (if run)
        if not e2e_results.get("skipped", False):
            for form_type, result in e2e_results.items():
                all_tests.append(result.get("success", False))
        
        passed_tests = sum(all_tests)
        total_tests = len(all_tests)
        success_rate = passed_tests / total_tests if total_tests > 0 else 0
        
        summary = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "success_rate": success_rate,
            "total_time": total_time,
            "test_suites": {
                "transcript_quality": transcript_results,
                "routing_logic": routing_results,
                "form_compatibility": compatibility_results,
                "end_to_end": e2e_results
            }
        }
        
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST SUMMARY")
        print(f"✅ Passed: {passed_tests}/{total_tests} ({success_rate:.1%})")
        print(f"⏱️  Total Time: {total_time:.2f}s")
        print(f"🎯 Form Types Tested: {len(FORM_TRANSCRIPTS)}")
        print("=" * 60)
        
        return summary


def main():
    """Main testing function"""
    
    # Determine if we should run API tests
    run_api_tests = "--api" in sys.argv
    
    if run_api_tests:
        print("🚨 API testing enabled - this will make actual API calls")
    else:
        print("🔍 Running non-API tests only (use --api for full testing)")
    
    # Create tester and run tests
    tester = FormsPipelineTester(run_api_tests=run_api_tests)
    results = tester.run_all_tests()
    
    # Save results
    import json
    results_file = f"form_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Convert any non-serializable objects
    def make_serializable(obj):
        if hasattr(obj, 'value'):
            return obj.value
        return obj
    
    serializable_results = json.loads(json.dumps(results, default=make_serializable))
    
    with open(results_file, 'w') as f:
        json.dump(serializable_results, f, indent=2)
    
    print(f"📁 Results saved to: {results_file}")
    
    return results


if __name__ == "__main__":
    main()