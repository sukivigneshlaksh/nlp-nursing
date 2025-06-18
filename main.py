import streamlit as st
from dotenv import load_dotenv
import openai
import os
from form_files.simple_form import MedicalHistoryForm, sample_transcript
from form_files.cms_form import CMSPAPDeviceForm, sample_cms_transcript
from form_files.prior_auth_form import PriorAuthForm, sample_prior_auth_transcript
from form_files.wellness_form import WellnessVisitForm, sample_wellness_transcript

# Page config
st.set_page_config(
    page_title="Medical Form Processor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Form configurations
FORMS = {
    "Medical History": {
        "model": MedicalHistoryForm,
        "transcript": sample_transcript,
        "status": "active",
        "display_func": "display_medical_history"
    },
    "CMS PAP Device": {
        "model": CMSPAPDeviceForm,
        "transcript": sample_cms_transcript,
        "status": "active",
        "display_func": "display_cms_form"
    },
    "Prior Authorization": {
        "model": PriorAuthForm,
        "transcript": sample_prior_auth_transcript,
        "status": "active",
        "display_func": "display_prior_auth"
    },
    "Medicare Wellness": {
        "model": WellnessVisitForm,
        "transcript": sample_wellness_transcript,
        "status": "active",
        "display_func": "display_wellness"
    }
}

def extract_medical_data(transcript, model_class):
    """Extract structured medical data from transcript using OpenAI API"""
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Extract medical form data from transcript. Only use explicitly mentioned information."},
            {"role": "user", "content": transcript}
        ],
        response_format=model_class,
    )
    return response.choices[0].message.parsed

def display_results(data):
    """Display extracted data in clean format"""
    
    # Basic Information
    with st.container():
        st.markdown("### Patient Information")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Name", data.name or "Not provided")
        with col2:
            st.metric("Age", data.age or "Not provided")
        with col3:
            st.metric("County", data.county_of_residence or "Not provided")
        with col4:
            st.metric("Form Date", data.form_date or "Not provided")
    
    st.divider()
    
    # Current Doctor
    st.markdown("### Current Doctor")
    st.write(data.current_doctor or "Not provided")
    
    st.divider()
    
    # Medical Problems
    st.markdown("### Medical Problems")
    if data.major_medical_problems:
        for problem in data.major_medical_problems:
            st.write(f"• {problem}")
    else:
        st.write("None reported")
    
    st.divider()
    
    # Medications
    st.markdown("### Current Medications")
    if data.current_medications:
        for med in data.current_medications:
            st.write(f"**{med.name}** — {med.purpose or 'Purpose not specified'}")
    else:
        st.write("None reported")
    
    st.divider()
    
    # Hospitalizations
    st.markdown("### Hospitalizations")
    if data.hospitalizations:
        for hosp in data.hospitalizations:
            st.write(f"**{hosp.hospital}** ({hosp.date_text}) — {hosp.reason}")
    else:
        st.write("None reported")
    
    st.divider()
    
    # Surgeries
    st.markdown("### Surgeries")
    if data.surgeries:
        for surgery in data.surgeries:
            st.write(f"**{surgery.procedure}** — {surgery.date_text}")
    else:
        st.write("None reported")

def display_cms_results(data):
    """Display CMS PAP Device form results"""
    
    # Patient Information
    if data.patient_info:
        st.markdown("### Patient Information")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Name", data.patient_info.name or "Not provided")
        with col2:
            st.metric("DOB", data.patient_info.date_of_birth or "Not provided")
        with col3:
            st.metric("Sex", data.patient_info.sex or "Not provided")
        with col4:
            st.metric("HICN", data.patient_info.hicn or "Not provided")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Height (in)", data.patient_info.height_inches or "Not provided")
        with col2:
            st.metric("Weight (lbs)", data.patient_info.weight_pounds or "Not provided")
        with col3:
            st.metric("Phone", data.patient_info.telephone or "Not provided")
    
    st.divider()
    
    # Certification Info
    st.markdown("### Certification Details")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Type:** {data.certification_type or 'Not specified'}")
        st.write(f"**Date:** {data.certification_date or 'Not specified'}")
    with col2:
        st.write(f"**Length of Need:** {data.estimated_length_of_need or 'Not specified'} months")
        st.write(f"**Diagnosis Codes:** {', '.join(data.diagnosis_codes) if data.diagnosis_codes else 'Not provided'}")
    
    st.divider()
    
    # Physician Information
    if data.physician_info:
        st.markdown("### Physician Information")
        st.write(f"**Name:** {data.physician_info.name or 'Not provided'}")
        st.write(f"**NPI:** {data.physician_info.nsc_or_npi or 'Not provided'}")
        st.write(f"**Phone:** {data.physician_info.telephone or 'Not provided'}")
    
    st.divider()
    
    # Clinical Questions
    if data.clinical_questions:
        st.markdown("### Clinical Assessment")
        clinical = data.clinical_questions
        
        st.write(f"**Obstructive Sleep Apnea Treatment:** {'Yes' if clinical.obstructive_sleep_apnea_treatment == 'Y' else 'No' if clinical.obstructive_sleep_apnea_treatment == 'N' else 'Not specified'}")
        st.write(f"**Initial Evaluation Date:** {clinical.initial_face_to_face_date or 'Not provided'}")
        st.write(f"**Sleep Test Date:** {clinical.sleep_test_date or 'Not provided'}")
        st.write(f"**Facility-Based Test:** {'Yes' if clinical.facility_based_sleep_test == 'Y' else 'No' if clinical.facility_based_sleep_test == 'N' else 'Not specified'}")
        st.write(f"**AHI/RDI Value:** {clinical.ahi_or_rdi_value or 'Not provided'}")
        st.write(f"**Documented Symptoms:** {'Yes' if clinical.documented_symptoms == 'Y' else 'No' if clinical.documented_symptoms == 'N' else 'Not specified'}")
    
    st.divider()
    
    # Equipment
    st.markdown("### Equipment")
    st.write(f"**Description:** {data.equipment_description or 'Not provided'}")
    if data.hcpcs_codes:
        st.write(f"**HCPCS Codes:** {', '.join(data.hcpcs_codes)}")

def display_prior_auth_results(data):
    """Display Prior Authorization form results"""
    
    # Member Information
    if data.member_info:
        st.markdown("### Member Information")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Name", data.member_info.name or "Not provided")
        with col2:
            st.metric("Member ID", data.member_info.member_id or "Not provided")
        with col3:
            st.metric("DOB", data.member_info.date_of_birth or "Not provided")
        with col4:
            st.metric("Phone", data.member_info.phone or "Not provided")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Address:** {data.member_info.street_address or 'Not provided'}")
            st.write(f"**City, State ZIP:** {data.member_info.city or ''} {data.member_info.state or ''} {data.member_info.zip_code or ''}")
        with col2:
            st.write(f"**Allergies:** {data.member_info.allergies or 'None reported'}")
    
    st.divider()
    
    # Request Details
    st.markdown("### Request Details")
    col1, col2 = st.columns(2)
    with col1:
        med_type = data.medication_type.value if data.medication_type else "Not specified"
        st.write(f"**Medication Type:** {med_type}")
        hosp_status = data.currently_hospitalized.value if data.currently_hospitalized else "Not specified"
        st.write(f"**Currently Hospitalized:** {hosp_status}")
    with col2:
        if data.therapy_start_date:
            st.write(f"**Therapy Start Date:** {data.therapy_start_date}")
        pregnant_status = data.member_pregnant.value if data.member_pregnant else "Not specified"
        st.write(f"**Member Pregnant:** {pregnant_status}")
    
    st.divider()
    
    # Prescriber Information
    if data.prescriber_info:
        st.markdown("### Prescriber Information")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**Provider:** {data.prescriber_info.provider_name or 'Not provided'}")
            st.write(f"**Specialty:** {data.prescriber_info.specialty or 'Not provided'}")
        with col2:
            st.write(f"**NPI:** {data.prescriber_info.npi_number or 'Not provided'}")
            st.write(f"**Phone:** {data.prescriber_info.office_phone or 'Not provided'}")
        with col3:
            st.write(f"**Fax:** {data.prescriber_info.office_fax or 'Not provided'}")
    
    st.divider()
    
    # Medication Information
    if data.medication_info:
        st.markdown("### Medication Information")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Medication:** {data.medication_info.medication_name or 'Not provided'}")
            st.write(f"**Strength:** {data.medication_info.strength or 'Not provided'}")
            st.write(f"**Quantity:** {data.medication_info.quantity or 'Not provided'}")
        with col2:
            st.write(f"**Directions:** {data.medication_info.directions_for_use or 'Not provided'}")
            admin_method = data.medication_info.medication_administered.value if data.medication_info.medication_administered else "Not specified"
            st.write(f"**Administration:** {admin_method}")
    
    st.divider()
    
    # Clinical Information
    if data.clinical_info:
        st.markdown("### Clinical Information")
        st.write(f"**Diagnosis:** {data.clinical_info.diagnosis or 'Not provided'}")
        if data.clinical_info.icd10_codes:
            st.write(f"**ICD-10 Codes:** {', '.join(data.clinical_info.icd10_codes)}")
        
        if data.clinical_info.medication_failures:
            st.markdown("**Previous Medication Failures:**")
            st.write(data.clinical_info.medication_failures)
        
        if data.clinical_info.contraindications_intolerances:
            st.markdown("**Contraindications/Intolerances:**")
            st.write(data.clinical_info.contraindications_intolerances)
        
        if data.clinical_info.lab_test_results:
            st.markdown("**Lab/Test Results:**")
            st.write(data.clinical_info.lab_test_results)
        
        if data.clinical_info.additional_information:
            st.markdown("**Additional Information:**")
            st.write(data.clinical_info.additional_information)

def display_wellness_results(data):
    """Display Medicare Wellness Visit form results"""
    
    # Basic Information
    if data.basic_info:
        st.markdown("### Patient Information")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Name", data.basic_info.name or "Not provided")
        with col2:
            st.metric("Birth Date", data.basic_info.birthdate or "Not provided")
        with col3:
            st.metric("Visit Date", data.basic_info.todays_date or "Not provided")
    
    st.divider()
    
    # Self Assessment
    if data.self_assessment:
        st.markdown("### Health Self-Assessment")
        col1, col2 = st.columns(2)
        with col1:
            health_rating = data.self_assessment.overall_health_rating.value if data.self_assessment.overall_health_rating else "Not specified"
            st.write(f"**Overall Health Rating:** {health_rating}")
            can_manage = data.self_assessment.can_manage_health_problems.value if data.self_assessment.can_manage_health_problems else "Not specified"
            st.write(f"**Can Manage Health Problems:** {can_manage}")
        with col2:
            needs_help = data.self_assessment.needs_help_personal_care.value if data.self_assessment.needs_help_personal_care else "Not specified"
            st.write(f"**Needs Help with Personal Care:** {needs_help}")
            emotional_support = data.self_assessment.emotional_support.value if data.self_assessment.emotional_support else "Not specified"
            st.write(f"**Emotional Support:** {emotional_support}")
    
    st.divider()
    
    # Health Habits
    if data.health_habits:
        st.markdown("### Health & Exercise Habits")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Exercise Days/Week", data.health_habits.exercise_days_per_week or "Not provided")
            st.metric("Exercise Minutes", data.health_habits.exercise_minutes or "Not provided")
        with col2:
            intensity = data.health_habits.exercise_intensity.value if data.health_habits.exercise_intensity else "Not specified"
            st.write(f"**Exercise Intensity:** {intensity}")
            fruits_veggies = data.health_habits.fruits_vegetables_frequency.value if data.health_habits.fruits_vegetables_frequency else "Not specified"
            st.write(f"**Fruits/Vegetables:** {fruits_veggies}")
        with col3:
            fiber = data.health_habits.high_fiber_frequency.value if data.health_habits.high_fiber_frequency else "Not specified"
            st.write(f"**High Fiber Foods:** {fiber}")
            teeth = data.health_habits.mouth_teeth_condition.value if data.health_habits.mouth_teeth_condition else "Not specified"
            st.write(f"**Dental Health:** {teeth}")
    
    st.divider()
    
    # Function and Mobility
    if data.function_mobility:
        st.markdown("### Function & Mobility")
        
        # Basic ADLs
        st.markdown("**Activities of Daily Living:**")
        col1, col2 = st.columns(2)
        with col1:
            bathing = data.function_mobility.bathing.value if data.function_mobility.bathing else "Not specified"
            st.write(f"• **Bathing:** {bathing}")
            dressing = data.function_mobility.getting_dressed.value if data.function_mobility.getting_dressed else "Not specified"
            st.write(f"• **Dressing:** {dressing}")
            toilet = data.function_mobility.using_toilet.value if data.function_mobility.using_toilet else "Not specified"
            st.write(f"• **Using Toilet:** {toilet}")
        with col2:
            eating = data.function_mobility.preparing_food_eating.value if data.function_mobility.preparing_food_eating else "Not specified"
            st.write(f"• **Preparing Food/Eating:** {eating}")
            moving = data.function_mobility.moving_around.value if data.function_mobility.moving_around else "Not specified"
            st.write(f"• **Moving Around:** {moving}")
        
        # Safety
        st.markdown("**Safety & Falls:**")
        col1, col2 = st.columns(2)
        with col1:
            falls = data.function_mobility.fallen_or_near_fall.value if data.function_mobility.fallen_or_near_fall else "Not specified"
            st.write(f"**Recent Falls:** {falls}")
            afraid = data.function_mobility.afraid_of_falling.value if data.function_mobility.afraid_of_falling else "Not specified"
            st.write(f"**Afraid of Falling:** {afraid}")
        with col2:
            balance = data.function_mobility.balance_issues.value if data.function_mobility.balance_issues else "Not specified"
            st.write(f"**Balance Issues:** {balance}")
            safe_home = data.function_mobility.feels_safe_at_home.value if data.function_mobility.feels_safe_at_home else "Not specified"
            st.write(f"**Feels Safe at Home:** {safe_home}")
        
        # Assistive devices
        if data.function_mobility.assistive_devices:
            st.write(f"**Assistive Devices:** {', '.join(data.function_mobility.assistive_devices)}")
    
    st.divider()
    
    # Memory Assessment
    if data.memory_assessment:
        st.markdown("### Memory Assessment")
        col1, col2 = st.columns(2)
        with col1:
            memory_issues = data.memory_assessment.memory_issues.value if data.memory_assessment.memory_issues else "Not specified"
            st.write(f"**Memory Issues:** {memory_issues}")
        with col2:
            concerns = data.memory_assessment.concerns_raised_by_others.value if data.memory_assessment.concerns_raised_by_others else "Not specified"
            st.write(f"**Others' Concerns:** {concerns}")
    
    st.divider()
    
    # Preventive Services
    if data.preventive_services:
        st.markdown("### Recent Preventive Care")
        
        # Show key screenings
        if data.preventive_services.mammogram and data.preventive_services.mammogram.when_completed:
            st.write(f"**Mammogram:** {data.preventive_services.mammogram.when_completed} at {data.preventive_services.mammogram.where_completed or 'Unknown location'}")
        
        if data.preventive_services.colorectal_screening and data.preventive_services.colorectal_screening.when_completed:
            st.write(f"**Colonoscopy:** {data.preventive_services.colorectal_screening.when_completed} at {data.preventive_services.colorectal_screening.where_completed or 'Unknown location'}")
        
        if data.preventive_services.bone_density and data.preventive_services.bone_density.when_completed:
            results = data.preventive_services.bone_density.results_normal.value if data.preventive_services.bone_density.results_normal else "Unknown results"
            st.write(f"**Bone Density:** {data.preventive_services.bone_density.when_completed} - Results: {results}")
        
        if data.preventive_services.eye_exam and data.preventive_services.eye_exam.when_completed:
            st.write(f"**Eye Exam:** {data.preventive_services.eye_exam.when_completed} at {data.preventive_services.eye_exam.where_completed or 'Unknown location'}")
    
    st.divider()
    
    # Advance Care Planning
    if data.advance_care_planning:
        st.markdown("### Advance Care Planning")
        col1, col2 = st.columns(2)
        with col1:
            living_will = data.advance_care_planning.has_living_will.value if data.advance_care_planning.has_living_will else "Not specified"
            st.write(f"**Living Will:** {living_will}")
            poa = data.advance_care_planning.has_power_of_attorney.value if data.advance_care_planning.has_power_of_attorney else "Not specified"
            st.write(f"**Power of Attorney:** {poa}")
        with col2:
            polst = data.advance_care_planning.has_polst.value if data.advance_care_planning.has_polst else "Not specified"
            st.write(f"**POLST Form:** {polst}")
            discuss = data.advance_care_planning.wants_to_discuss.value if data.advance_care_planning.wants_to_discuss else "Not specified"
            st.write(f"**Wants to Discuss:** {discuss}")

def get_display_function(form_name):
    """Return appropriate display function based on form type"""
    if form_name == "Medical History":
        return display_results
    elif form_name == "CMS PAP Device":
        return display_cms_results
    elif form_name == "Prior Authorization":
        return display_prior_auth_results
    elif form_name == "Medicare Wellness":
        return display_wellness_results
    else:
        return display_results  # fallback

def main():
    # Header
    st.markdown("# Medical Form Processor")
    st.markdown("Extract structured data from medical transcripts using AI")
    
    st.markdown("---")
    
    # Form selection
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("### Select Form")
        selected_form = st.radio(
            "",
            options=list(FORMS.keys()),
            label_visibility="collapsed"
        )
    
    with col2:
        form_config = FORMS[selected_form]
        
        if form_config["status"] == "coming_soon":
            st.markdown("### Coming Soon")
            st.info(f"{selected_form} form is currently in development.")
            return
        
        st.markdown(f"### {selected_form} Form")
        
        # Transcript display
        with st.expander("View Sample Transcript"):
            st.code(form_config["transcript"], language="text")
        
        # Process button
        if st.button("Process Transcript", type="primary", use_container_width=True):
            with st.spinner("Processing..."):
                try:
                    extracted_data = extract_medical_data(form_config["transcript"], form_config["model"])
                    st.success("Processing complete")
                    
                    st.markdown("---")
                    st.markdown("## Extracted Data")
                    
                    # Use appropriate display function
                    display_func = get_display_function(selected_form)
                    display_func(extracted_data)
                    
                except Exception as e:
                    st.error(f"Processing failed: {str(e)}")

if __name__ == "__main__":
    main()