"""
Minimal Medical Form Processor Demo
"""

import streamlit as st
import json
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

st.title("Medical Form Processor")

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
            
            # JSON Output
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