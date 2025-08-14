"""
Suki AI Internship Demo
Shows progression: basic API → agentic → concurrent processing
"""

from pdf_ingestion import demonstrate_basic_pdf_ingestion
from medical_data_structures import demonstrate_data_structures  
from llm_api_processor import demonstrate_basic_llm_api_processing
from agentic_extraction import demonstrate_agentic_extraction
from concurrent_processor import demonstrate_concurrency_progression


def main():
    """Run complete demonstration of Suki AI internship work."""
    print("🏥 SUKI AI MEDICAL DOCUMENT PROCESSING DEMO")
    print("Demonstrating internship progression and concurrency concepts")
    print("=" * 70)
    
    # Stage 1: Basic PDF ingestion
    print("\n📄 STAGE 1: PDF INGESTION")
    demonstrate_basic_pdf_ingestion()
    
    # Stage 2: Data structures  
    print("\n🏗️  STAGE 2: MEDICAL DATA STRUCTURES")
    demonstrate_data_structures()
    
    # Stage 3: Basic LLM API
    print("\n🤖 STAGE 3: LLM API PROCESSING") 
    demonstrate_basic_llm_api_processing()
    
    # Stage 4: Agentic processing
    print("\n🎯 STAGE 4: AGENTIC EXTRACTION")
    demonstrate_agentic_extraction()
    
    # Stage 5: Concurrent processing
    print("\n⚡ STAGE 5: CONCURRENT PROCESSING")
    demonstrate_concurrency_progression()
    
    print("\n" + "="*70)
    print("INTERNSHIP PROGRESSION COMPLETE")
    print("Key insights:")
    print("• Started with basic PDF text extraction")
    print("• Built structured medical data representations") 
    print("• Integrated LLM APIs for intelligent extraction")
    print("• Added agentic planning and execution")
    print("• Applied GPU-inspired concurrency for scale")
    print("• Future: Tasks become simple enough for single API calls")
    print("="*70)


if __name__ == "__main__":
    main()