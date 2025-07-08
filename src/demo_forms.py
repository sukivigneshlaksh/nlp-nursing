"""
Demo: Form-Specific Processing
=============================

Demonstrates how to use the end-to-end pipeline with different form types
and their corresponding transcripts.

Usage:
    python demo_forms.py [form_type]
    
    form_type options:
    - simple_form
    - cms_form
    - prior_auth_form
    - pain_assessment
    - wellness_form
    - all (process all forms)
"""

import sys
import json
from datetime import datetime
from form_transcripts import FORM_TRANSCRIPTS, FORM_TEST_CASES, get_transcript_for_form


def demo_transcript_analysis():
    """Demo transcript analysis without API calls"""
    
    print("🏥 MEDICAL FORM TRANSCRIPTS DEMO")
    print("=" * 50)
    
    for i, (form_type, transcript) in enumerate(FORM_TRANSCRIPTS.items(), 1):
        print(f"\n{i}. {form_type.upper().replace('_', ' ')}")
        print("-" * 30)
        
        # Basic analysis
        word_count = len(transcript.split())
        lines = transcript.strip().split('\n')
        dialogue_lines = len([line for line in lines if ':' in line])
        
        print(f"📊 Length: {word_count} words, {len(lines)} lines")
        print(f"💬 Dialogue: {dialogue_lines} exchanges")
        
        # Find key participants
        participants = set()
        for line in lines:
            if ':' in line:
                speaker = line.split(':')[0].strip()
                if speaker in ['NURSE', 'DOCTOR', 'PATIENT', 'A']:
                    participants.add(speaker)
        
        print(f"👥 Participants: {', '.join(participants)}")
        
        # Show first few lines as preview
        preview_lines = [line.strip() for line in lines[:5] if line.strip()]
        print(f"📋 Preview:")
        for line in preview_lines:
            if len(line) > 60:
                line = line[:60] + "..."
            print(f"   {line}")
        
        print()


def demo_form_routing():
    """Demo form routing logic"""
    
    print("\n🧭 FORM ROUTING DEMONSTRATION")
    print("=" * 50)
    
    for test_case in FORM_TEST_CASES:
        form_type = test_case["form_type"]
        expected_complexity = test_case["expected_complexity"]
        pdf_path = test_case["pdf_path"]
        
        print(f"\n📄 {test_case['name']}")
        print(f"   Type: {form_type}")
        print(f"   PDF: {pdf_path}")
        print(f"   Complexity: {expected_complexity}")
        
        # Recommended processing approach
        if expected_complexity == "simple":
            approach = "🚀 Fast Track (1-2 API calls)"
            strategy = "Single model creation + filling"
        else:
            approach = "🔄 Complex Processing (disjoint sections + concurrency)"
            strategy = "Section identification → parallel processing"
        
        print(f"   Approach: {approach}")
        print(f"   Strategy: {strategy}")


def demo_specific_form(form_type: str):
    """Demo processing for a specific form type"""
    
    if form_type not in FORM_TRANSCRIPTS:
        print(f"❌ Unknown form type: {form_type}")
        print(f"Available types: {list(FORM_TRANSCRIPTS.keys())}")
        return
    
    print(f"\n🎯 PROCESSING DEMO: {form_type.upper()}")
    print("=" * 50)
    
    # Get transcript and test case
    transcript = get_transcript_for_form(form_type)
    test_case = next((tc for tc in FORM_TEST_CASES if tc['form_type'] == form_type), {})
    
    # Show form details
    print(f"📋 Form: {test_case.get('name', 'Unknown')}")
    print(f"📄 PDF: {test_case.get('pdf_path', 'N/A')}")
    print(f"🎯 Complexity: {test_case.get('expected_complexity', 'unknown')}")
    print(f"📊 Transcript: {len(transcript.split())} words")
    
    # Show key fields that should be extracted
    key_fields = test_case.get('key_fields', [])
    if key_fields:
        print(f"\n🔍 Key Fields to Extract:")
        for field in key_fields:
            print(f"   • {field}")
    
    # Show transcript excerpt
    print(f"\n💬 Transcript Excerpt:")
    lines = transcript.strip().split('\n')
    excerpt_lines = [line.strip() for line in lines[1:15] if line.strip()]  # Skip header
    
    for line in excerpt_lines:
        if len(line) > 80:
            line = line[:80] + "..."
        print(f"   {line}")
    
    # Show processing strategy
    print(f"\n⚙️ Processing Strategy:")
    if test_case.get('expected_complexity') == 'simple':
        print("   1. 🔍 Analyze PDF structure (simple)")
        print("   2. 📝 Create complete form model (1 API call)")
        print("   3. 📊 Fill model with transcript data (1 API call)")
        print("   4. 💾 Generate outputs (JSON + report)")
        print("   ⏱️  Estimated time: 10-15 seconds")
    else:
        print("   1. 🔍 Analyze PDF and extract chunks")
        print("   2. 🧩 Identify disjoint sections (1 API call)")
        print("   3. 🔄 Process sections concurrently (N API calls)")
        print("   4. 🔗 Combine section results")
        print("   5. 💾 Generate outputs (JSON + report)")
        print("   ⏱️  Estimated time: 30-60 seconds")
    
    # Simulated processing output
    print(f"\n📤 Expected Output Structure:")
    if form_type == "simple_form":
        output_example = {
            "name": "Maria Elena Rodriguez",
            "age": 62,
            "county_of_residence": "Orange County",
            "major_medical_problems": ["Type 2 diabetes", "Hypertension", "Hyperlipidemia"],
            "current_medications": [
                {"name": "Metformin", "purpose": "diabetes"},
                {"name": "Lisinopril", "purpose": "blood pressure"}
            ]
        }
    elif form_type == "cms_form":
        output_example = {
            "patient_info": {"name": "Robert James Thompson", "hicn": "1EG4-TE5-MK89"},
            "physician_info": {"name": "Dr. Michael Chen", "specialty": "Sleep Medicine"},
            "clinical_questions": {"obstructive_sleep_apnea_treatment": "Y", "ahi_or_rdi_value": "28"}
        }
    else:
        output_example = {"form_data": "Structured based on form type"}
    
    print(json.dumps(output_example, indent=2))


def main():
    """Main demo function"""
    
    if len(sys.argv) < 2:
        print("Usage: python demo_forms.py [form_type|all]")
        print(f"Available form types: {list(FORM_TRANSCRIPTS.keys())}")
        return
    
    form_type = sys.argv[1].lower()
    
    if form_type == "all":
        demo_transcript_analysis()
        demo_form_routing()
        
        print("\n" + "=" * 50)
        print("🎯 INDIVIDUAL FORM DEMOS")
        print("=" * 50)
        
        for ft in FORM_TRANSCRIPTS.keys():
            demo_specific_form(ft)
            print()
    
    elif form_type in FORM_TRANSCRIPTS:
        demo_specific_form(form_type)
    
    else:
        print(f"❌ Unknown form type: {form_type}")
        print(f"Available types: {list(FORM_TRANSCRIPTS.keys())}")
        print("Use 'all' to see all forms")


if __name__ == "__main__":
    main()