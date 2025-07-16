"""
Medical Form Processor Demo with Enhanced Output Display
"""

import streamlit as st
import json
import pandas as pd
from models3 import process_form_with_openai
from models import (
    MedicalHistory,
    CMSPAPDeviceForm, 
    PriorAuthorizationRequest,
    MedicareWellnessAssessment
)
from form_transcripts import (
    SIMPLE_FORM_TRANSCRIPT,
    CMS_FORM_TRANSCRIPT,
    PRIOR_AUTH_TRANSCRIPT,
    WELLNESS_FORM_TRANSCRIPT
)

st.title("Medical Form Processor with Enhanced Display")

# Form configurations
FORMS = {
    "Simple Medical History": (MedicalHistory, SIMPLE_FORM_TRANSCRIPT),
    "CMS PAP Device": (CMSPAPDeviceForm, CMS_FORM_TRANSCRIPT),
    "Prior Authorization": (PriorAuthorizationRequest, PRIOR_AUTH_TRANSCRIPT),
    "Medicare Wellness": (MedicareWellnessAssessment, WELLNESS_FORM_TRANSCRIPT)
}

# Form selection
selected_form = st.selectbox("Select Form:", list(FORMS.keys()))
model, transcript = FORMS[selected_form]

# Show full transcript
st.subheader("Medical Transcript")
st.text_area("", value=transcript, height=300, disabled=True)

# Process button
if st.button("Process Form", type="primary"):
    with st.spinner("Processing..."):
        try:
            result = process_form_with_openai(transcript, model)
            st.success("Processing completed!")
            
            # Create tabs for different output representations
            tab1, tab2 = st.tabs(["Key-Value Table", "JSON Output"])
            
            with tab1:
                st.subheader("Key-Value Table")
                
                def flatten_dict(d, parent_key='', sep='_'):
                    """Flatten nested dictionary for table display"""
                    items = []
                    for k, v in d.items():
                        new_key = f"{parent_key}{sep}{k}" if parent_key else k
                        if isinstance(v, dict):
                            items.extend(flatten_dict(v, new_key, sep=sep).items())
                        elif isinstance(v, list):
                            if v:
                                for i, item in enumerate(v):
                                    if isinstance(item, dict):
                                        items.extend(flatten_dict(item, f"{new_key}_{i}", sep=sep).items())
                                    else:
                                        items.append((f"{new_key}_{i}", str(item)))
                            else:
                                items.append((new_key, "None"))
                        else:
                            items.append((new_key, str(v)))
                    return dict(items)
                
                flattened = flatten_dict(result.model_dump())
                df = pd.DataFrame([
                    {"Field": k.replace('_', ' ').title(), "Value": v} 
                    for k, v in flattened.items()
                ])
                st.dataframe(df, use_container_width=True)
            
            with tab2:
                st.subheader("JSON Output")
                st.json(result.model_dump())
            
            # Download button
            json_str = json.dumps(result.model_dump(), indent=2)
            st.download_button(
                "Download JSON",
                json_str,
                f"{selected_form.lower().replace(' ', '_')}.json",
                "application/json"
            )
            
        except Exception as e:
            st.error(f"Error: {e}")