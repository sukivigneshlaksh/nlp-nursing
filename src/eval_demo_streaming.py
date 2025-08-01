import streamlit as st
import json
from medical_form_utils import (
    load_template, extract_with_citations, 
    load_sample_transcript, get_field_values, format_field_name,
    evaluate_citations, get_basic_metrics
)
from whisper_audio import SimpleWhisperStreamer

# Initialize Whisper streamer in session state
if 'whisper_streamer' not in st.session_state:
    st.session_state.whisper_streamer = SimpleWhisperStreamer()

# Main UI
st.title("Medical Form Demo with Streaming Audio")

# Load form templates
cms_template = load_template("../outputs/cms_output.json")
oasis_template = load_template("../outputs/oasis_output_short.json")

# Form selection
form_type = st.radio("Choose Form:", ["CMS", "OASIS"])
normalized_form_type = "CMS" if form_type == "CMS" else "OASIS"

# Audio recording section
st.subheader("Audio Input")
col1, col2 = st.columns([1, 3])

with col1:
    # Initialize recording state
    if 'is_recording' not in st.session_state:
        st.session_state.is_recording = False
    
    if not st.session_state.is_recording:
        if st.button("Start Recording"):
            st.session_state.is_recording = True
            st.session_state.whisper_streamer.start_recording()
            st.rerun()
    else:
        if st.button("Stop Recording"):
            st.session_state.is_recording = False
            with st.spinner("Processing audio..."):
                transcript = st.session_state.whisper_streamer.stop_recording()
                st.session_state.recorded_transcript = transcript
            st.success("Recording complete!")
            st.rerun()
        
        st.info("🎤 Recording in progress...")

with col2:
    # Load sample transcript as default
    sample_transcript = load_sample_transcript(normalized_form_type)
    # Fix path issue
    if "not found" in sample_transcript:
        sample_transcript = "Sample transcript: Patient reports pain level 8/10, difficulty walking, needs assistance with daily activities."
    
    # Use recorded transcript if available, otherwise sample
    default_transcript = st.session_state.get('recorded_transcript', sample_transcript)
    transcript = st.text_area("Medical Transcript:", value=default_transcript, height=300)

# Process button
if st.button("Extract Data & Evaluate"):
    template = cms_template if form_type == "CMS" else oasis_template
    
    with st.spinner("Processing..."):
        # Single call: extract directly into template with citations
        citation_data = extract_with_citations(transcript, template, form_type)
        
        # Extract components
        filled = citation_data.get("filled_form", {})
        
        # Evaluate using existing citation data
        evaluation = evaluate_citations(citation_data)
    
    # Display metrics at the top
    st.success("Processing Complete")
    
    # Metrics dashboard
    metrics = evaluation["metrics"]
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Coverage", f"{metrics['coverage_percentage']:.1f}%", 
                 f"{metrics['filled_fields']}/{metrics['total_fields']} fields")
    
    with col2:
        st.metric("Overall Quality", f"{metrics['overall_quality']}/10")
    
    with col3:
        st.metric("Filled Fields", metrics['filled_fields'])
    
    with col4:
        st.metric("Empty Fields", metrics['empty_fields'])
    
    # Field Analysis Section
    st.subheader("Field Analysis")
    
    # Check if citations exist in raw data
    citations = citation_data.get("citations", {})
    
    if not citations:
        st.info("No citations provided - showing basic field coverage only")
        # Show basic field analysis without confidence scores
        filled_fields = get_field_values(filled)
        
        if filled_fields:
            st.write("**Filled Fields:**")
            for field_path, value in filled_fields.items():
                st.write(f"{format_field_name(field_path)}: {value}")
        else:
            st.warning("No fields were filled from the transcript")
    else:
        field_analysis = evaluation.get("field_analysis", {})
        
        if field_analysis and len(field_analysis) > 0:
            # Create confidence score overview
            confidence_scores = [data.get("confidence", 0) for data in field_analysis.values()]
            avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        
            st.metric("Average Confidence", f"{avg_confidence:.1f}/10")
            
            # Detailed field breakdown
            for field_path, analysis in field_analysis.items():
                with st.expander(f"{format_field_name(field_path)} (Confidence: {analysis.get('confidence', 0)}/10)"):
                    col_a, col_b = st.columns([1, 2])
                
                    with col_a:
                        st.write("**Extracted Value:**")
                        field_values = get_field_values(filled)
                        st.code(field_values.get(field_path, "N/A"))
                        
                        confidence = analysis.get("confidence", 0)
                        if confidence >= 8:
                            st.success(f"High Confidence ({confidence}/10)")
                        elif confidence >= 6:
                            st.warning(f"Medium Confidence ({confidence}/10)")
                        else:
                            st.error(f"Low Confidence ({confidence}/10)")
                    
                    with col_b:
                        st.write("**Source Citation:**")
                        st.info(f'"{analysis.get("source_quote", "No citation provided")}"')
                        
                        issues = analysis.get("issues", "none")
                        if issues != "none":
                            st.warning(f"Issues: {issues}")
        else:
            st.info("Citations exist but field analysis is empty")
    
    # Original comparison section (collapsed by default)
    with st.expander("Form Comparison", expanded=False):
        original_fields = get_field_values(template)
        new_fields = get_field_values(filled)
        added_fields = {k: v for k, v in new_fields.items() if k not in original_fields}
        
        if added_fields:
            st.write("**Newly Extracted Data:**")
            for field, value in sorted(added_fields.items()):
                clean_field = format_field_name(field)
                st.text(f"{clean_field}: {value}")
        
        # Side-by-side comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Empty Template")
            st.json(template, expanded=False)
        
        with col2:
            st.subheader("Populated Form")  
            st.json(filled, expanded=False)
    
    # Download options
    st.subheader("Downloads")
    col_dl1, col_dl2 = st.columns(2)
    
    with col_dl1:
        st.download_button(
            "Download Filled Form",
            json.dumps(filled, indent=2),
            f"{form_type.lower()}_filled.json"
        )
    
    with col_dl2:
        st.download_button(
            "Download Evaluation Report",
            json.dumps(evaluation, indent=2),
            f"{form_type.lower()}_evaluation.json"
        )