import streamlit as st
import json
from medical_form_utils import (
    load_template, extract_with_ai, fill_form, 
    load_sample_transcript, get_field_values, format_field_name
)

# Main UI
st.title("Medical Form Demo")

# Load form templates
cms_template = load_template("../outputs/cms_output.json")
oasis_template = load_template("../outputs/oasis_output_short.json")

# Form selection
form_type = st.radio("Choose Form:", ["CMS", "OASIS"])
normalized_form_type = "CMS" if form_type == "CMS" else "OASIS"

# Load and display transcript
sample_transcript = load_sample_transcript(normalized_form_type)
transcript = st.text_area("Medical Transcript:", value=sample_transcript, height=300)

# Process button
if st.button("Extract Data"):
    template = cms_template if form_type == "CMS" else oasis_template
    
    with st.spinner("Processing..."):
        extracted = extract_with_ai(transcript, form_type)
        filled = fill_form(template, extracted)
    
    # Compare filled vs empty
    original_fields = get_field_values(template)
    new_fields = get_field_values(filled)
    added_fields = {k: v for k, v in new_fields.items() if k not in original_fields}
    
    # Results
    st.success(f"Filled {len(added_fields)} additional fields")
    
    if added_fields:
        st.write("**Extracted Data:**")
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
    
    # Download option
    st.download_button(
        "Download Result",
        json.dumps(filled, indent=2),
        f"{form_type.lower().replace(' ', '_')}_filled.json"
    )