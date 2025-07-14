"""
NLP Nursing Form Processor - Real-time Demo
Minimal interface with live processing and thread monitoring.
"""

import streamlit as st
import json
import sys
from pathlib import Path
import pandas as pd
import queue
import time
from datetime import datetime
import io
import contextlib

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from agentic_doc_processor import process_single_pdf
    from form_transcripts import (
        SIMPLE_FORM_TRANSCRIPT, 
        CMS_FORM_TRANSCRIPT, 
        UHC_FORM_TRANSCRIPT, 
        WELLNESS_FORM_TRANSCRIPT
    )
    IMPORTS_AVAILABLE = True
except ImportError:
    IMPORTS_AVAILABLE = False

# Page config
st.set_page_config(
    page_title="NLP Form Processor",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Minimal CSS
st.markdown("""
<style>
    .metric-container {
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 4px;
        margin: 0.5rem 0;
    }
    
    .thread-status {
        font-family: monospace;
        background: #f8f9fa;
        padding: 0.5rem;
        border-radius: 4px;
        margin: 0.2rem 0;
        font-size: 0.85rem;
    }
    
    .processing { background: #fff3cd; }
    .complete { background: #d4edda; }
    .error { background: #f8d7da; }
</style>
""", unsafe_allow_html=True)


def extract_key_fields(result_json):
    """Extract only pertinent information from JSON result"""
    if not result_json:
        return {}
    
    key_info = {
        "form_name": result_json.get("form_name", "Unknown"),
        "total_sections": result_json.get("section_count", 0),
        "total_chunks": result_json.get("total_chunks", 0),
        "fields_extracted": [],
        "processing_time": "N/A"
    }
    
    # Extract filled fields only
    for section in result_json.get("disjoint_sections", []):
        kernel_output = section.get("kernel_output", {})
        filled_form = kernel_output.get("filled_form", {})
        section_type = filled_form.get("section_type", "unknown")
        
        for field in filled_form.get("fields", []):
            if field.get("value") is not None and field.get("value") != "":
                key_info["fields_extracted"].append({
                    "section": section_type,
                    "field": field.get("label", "Unknown"),
                    "value": str(field.get("value"))[:100] + ("..." if len(str(field.get("value"))) > 100 else "")
                })
    
    return key_info

def main():
    st.title("📋 NLP Form Processor")
    st.caption("Real-time agentic document processing with Landing AI + Vertex AI")
    
    if not IMPORTS_AVAILABLE:
        st.error("⚠️ Dependencies missing. Install: `pip install agentic-doc vertexai python-dotenv PyMuPDF streamlit`")
        return

    # Form configurations
    FORM_CONFIGS = {
        "Simple Medical History": {
            "name": "simple_form",
            "path": "data/pdf/Simple_Form.pdf",
            "transcript": SIMPLE_FORM_TRANSCRIPT
        },
        "CMS Certificate": {
            "name": "cms_form", 
            "path": "data/pdf/CMS_Form.pdf",
            "transcript": CMS_FORM_TRANSCRIPT
        },
        "UHC Prior Auth": {
            "name": "uhc_form",
            "path": "data/pdf/UHC_form.pdf", 
            "transcript": UHC_FORM_TRANSCRIPT
        },
        "Medicare Wellness": {
            "name": "wellness_form",
            "path": "data/pdf/Wellness_Form.pdf",
            "transcript": WELLNESS_FORM_TRANSCRIPT
        }
    }

    # Form selection
    st.subheader("Select Forms to Process")
    selected_forms = []
    
    cols = st.columns(4)
    for i, (form_name, config) in enumerate(FORM_CONFIGS.items()):
        with cols[i]:
            if st.checkbox(form_name, key=f"select_{config['name']}"):
                selected_forms.append((form_name, config))

    # Process button
    if st.button("🚀 Process Selected Forms", type="primary", disabled=len(selected_forms)==0):
        process_forms_realtime(selected_forms)

def process_forms_realtime(selected_forms):
    """Process forms sequentially with real-time monitoring"""
    if not selected_forms:
        return
    
    st.subheader("🔄 Live Processing Monitor")
    
    # Create containers for live updates
    progress_container = st.container()
    status_container = st.container()
    
    with progress_container:
        progress_bar = st.progress(0)
        status_text = st.empty()
    
    with status_container:
        st.write("**Processing Status:**")
        status_display = st.empty()
    
    results = {}
    
    # Process each form sequentially
    for i, (form_name, config) in enumerate(selected_forms):
        # Update overall progress
        progress = i / len(selected_forms)
        progress_bar.progress(progress)
        status_text.text(f"Processing {i+1}/{len(selected_forms)}: {form_name}")
        
        # Show current form status
        with status_display:
            st.info(f"🔄 Processing {form_name}...")
        
        try:
            # Process the form
            result = process_single_pdf(
                pdf_path=config["path"],
                form_name=f"demo_{config['name']}",
                transcript=config["transcript"]
            )
            
            results[form_name] = (result, None)
            
            with status_display:
                st.success(f"✅ {form_name} completed - {result.get('section_count', 0)} sections processed")
                
        except Exception as e:
            results[form_name] = (None, str(e))
            
            with status_display:
                st.error(f"❌ {form_name} failed: {str(e)}")
        
        # Small delay to show status
        time.sleep(0.5)
    
    # Final update
    progress_bar.progress(1.0)
    status_text.text(f"✅ Completed all {len(selected_forms)} forms")
    
    # Display results
    display_results(results)

def display_results(results):
    """Display processing results with key information and download"""
    st.subheader("📊 Results")
    
    for form_name, (result, error) in results.items():
        with st.expander(f"📄 {form_name}", expanded=True):
            if error:
                st.error(f"Processing failed: {error}")
                continue
            
            if not result:
                st.warning("No result data available")
                continue
            
            # Extract key information
            key_info = extract_key_fields(result)
            
            # Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Sections", key_info["total_sections"])
            with col2:
                st.metric("Chunks", key_info["total_chunks"])
            with col3:
                st.metric("Fields Extracted", len(key_info["fields_extracted"]))
            
            # Show extracted fields
            if key_info["fields_extracted"]:
                st.write("**Extracted Data:**")
                
                # Create DataFrame for extracted fields
                df_data = []
                for field_info in key_info["fields_extracted"]:
                    df_data.append({
                        "Section": field_info["section"].replace("_", " ").title(),
                        "Field": field_info["field"],
                        "Value": field_info["value"]
                    })
                
                if df_data:
                    df = pd.DataFrame(df_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No field values were extracted from this form")
            
            # Download buttons
            col1, col2 = st.columns(2)
            
            with col1:
                # Download full JSON
                json_str = json.dumps(result, indent=2)
                st.download_button(
                    label="📥 Download Full JSON",
                    data=json_str,
                    file_name=f"{key_info['form_name']}_complete.json",
                    mime="application/json"
                )
            
            with col2:
                # Download key info only
                key_json_str = json.dumps(key_info, indent=2)
                st.download_button(
                    label="📥 Download Key Data",
                    data=key_json_str,
                    file_name=f"{key_info['form_name']}_summary.json",
                    mime="application/json"
                )

if __name__ == "__main__":
    main()