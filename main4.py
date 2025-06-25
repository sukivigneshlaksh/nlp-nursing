import openai
import os
from dotenv import load_dotenv
import json
from form_files.simple_form import MedicalHistoryForm, sample_transcript, MEDICAL_HISTORY_CLINICAL_WEIGHTS
from form_files.cms_form import CMSPAPDeviceForm, sample_cms_transcript, CMS_PAP_CLINICAL_WEIGHTS
from form_files.prior_auth_form import PriorAuthForm, sample_prior_auth_transcript, PRIOR_AUTH_CLINICAL_WEIGHTS
from form_files.wellness_form import WellnessVisitForm, sample_wellness_transcript, WELLNESS_VISIT_CLINICAL_WEIGHTS
from form_files.care_step import PainAssessmentForm, sample_pain_assessment_transcript, PAIN_ASSESSMENT_CLINICAL_WEIGHTS

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Form configurations with weights
FORMS = {
   "Medical History": {
       "model": MedicalHistoryForm,
       "transcript": sample_transcript,
       "weights": MEDICAL_HISTORY_CLINICAL_WEIGHTS
   },
   "CMS PAP Device": {
       "model": CMSPAPDeviceForm,
       "transcript": sample_cms_transcript,
       "weights": CMS_PAP_CLINICAL_WEIGHTS
   },
   "Prior Authorization": {
       "model": PriorAuthForm,
       "transcript": sample_prior_auth_transcript,
       "weights": PRIOR_AUTH_CLINICAL_WEIGHTS
   },
   "Medicare Wellness": {
       "model": WellnessVisitForm,
       "transcript": sample_wellness_transcript,
       "weights": WELLNESS_VISIT_CLINICAL_WEIGHTS
   },
   "Pain Assessment": {
       "model": PainAssessmentForm,
       "transcript": sample_pain_assessment_transcript,
       "weights": PAIN_ASSESSMENT_CLINICAL_WEIGHTS
   }
}

def extract_medical_data(transcript, model_class):
   """Extract structured medical data from transcript"""
   response = client.beta.chat.completions.parse(
       model="gpt-4.1",
       messages=[
           {"role": "system", "content": "Extract medical form data from transcript. Only use explicitly mentioned information."},
           {"role": "user", "content": transcript}
       ],
       response_format=model_class,
   )
   return response.choices[0].message.parsed

def flatten_data_for_weights(data_dict):
   """Convert nested dict to flat keys matching weight structure"""
   flattened = {}
   
   for key, value in data_dict.items():
       if isinstance(value, dict):
           for sub_key, sub_value in value.items():
               if isinstance(sub_value, dict):
                   # Handle nested dicts (like pain_location.area within PainLocationInfo)
                   for deep_key, deep_value in sub_value.items():
                       if isinstance(deep_value, list):
                           flattened[f"{key}.{sub_key}.{deep_key}"] = ', '.join(map(str, deep_value)) if deep_value else None
                       else:
                           flattened[f"{key}.{sub_key}.{deep_key}"] = deep_value
               elif isinstance(sub_value, list):
                   flattened[f"{key}.{sub_key}"] = ', '.join(map(str, sub_value)) if sub_value else None
               else:
                   flattened[f"{key}.{sub_key}"] = sub_value
       elif isinstance(value, list):
           flattened[key] = ', '.join(map(str, value)) if value else None
       else:
           flattened[key] = value
   
   return flattened

def evaluate_field(field_name, field_value, transcript):
   """Evaluate individual field extraction quality"""
   prompt = f"""
   Evaluate this field extraction from the medical transcript:
   
   Field: {field_name}
   Extracted Value: {field_value}
   
   Original Transcript: {transcript}
   
   Rate this field extraction (1-100 scale):
   - Accuracy: Is the extracted value correct?
   - Completeness: Was all relevant information captured?
   
   Respond with just a number between 1-100.
   """
   
   response = client.chat.completions.create(
       model="gpt-4.1",
       messages=[{"role": "user", "content": prompt}],
       max_tokens=10
   )
   
   try:
       score = int(response.choices[0].message.content.strip())
       return min(max(score, 1), 100)  # Clamp between 1-100
   except:
       return 50  # Default score if parsing fails

def evaluate_extraction_with_weights(extracted_data, transcript, weights):
   """Evaluate extraction quality with clinical weights using field-level weights"""
   field_evaluations = {}
   weighted_total = 0
   weight_sum = 0
   
   # Flatten data to match weight keys
   flattened_data = flatten_data_for_weights(extracted_data.model_dump())
   
   # Evaluate each field that has a weight
   for field_path, weight in weights.items():
       field_value = flattened_data.get(field_path)
       
       if field_value is not None:
           # Evaluate field
           score = evaluate_field(field_path, field_value, transcript)
           weighted_score = score * weight
           
           field_evaluations[field_path] = {
               "score": score,
               "weight": weight,
               "weighted_score": weighted_score,
               "value": field_value,
               "confidence": "high" if score >= 85 else "medium" if score >= 60 else "low"
           }
           
           weighted_total += weighted_score
           weight_sum += weight
   
   # Calculate overall weighted score
   overall_score = weighted_total / weight_sum if weight_sum > 0 else 0
   
   return {
       "overall_weighted_score": round(overall_score, 1),
       "field_evaluations": field_evaluations,
       "review_recommended": overall_score < 75
   }

def process_form(form_name):
   """Process individual form with weighted evaluation"""
   form_config = FORMS[form_name]
   
   print(f"\nProcessing {form_name}...")
   
   # Extract data
   extracted_data = extract_medical_data(form_config["transcript"], form_config["model"])
   
   # Evaluate with weights
   evaluation = evaluate_extraction_with_weights(
       extracted_data, 
       form_config["transcript"], 
       form_config["weights"]
   )
   
   # Combine results
   result = {
       "form_type": form_name,
       "extracted_data": extracted_data.model_dump(),
       "evaluation": evaluation
   }
   
   # Save to JSON
   filename = f"{form_name.lower().replace(' ', '_')}_weighted_results.json"
   with open(filename, "w") as f:
       json.dump(result, f, indent=2)
   
   print(f"Overall Score: {evaluation['overall_weighted_score']}")
   print(f"Review Recommended: {evaluation['review_recommended']}")
   
   # Print individual field performance if score is low
   if evaluation['overall_weighted_score'] < 85:
       print(f"Field-level issues:")
       for field_path, field_eval in evaluation['field_evaluations'].items():
           if field_eval['score'] < 85:
               print(f"  - {field_path}: {field_eval['score']} ({field_eval['confidence']}) - '{field_eval['value']}'")
   
   print(f"Saved to: {filename}")
   
   return result

def process_all_forms():
   """Process all forms with weighted evaluation"""
   print("Processing All Medical Forms with Weighted Evaluation")
   print("=" * 60)
   
   results = {}
   
   for form_name in FORMS.keys():
       results[form_name] = process_form(form_name)
   
   print("\n" + "=" * 60)
   print("SUMMARY")
   print("=" * 60)
   
   for form_name, result in results.items():
       score = result["evaluation"]["overall_weighted_score"]
       review = result["evaluation"]["review_recommended"]
       print(f"{form_name:<20}: {score:>5.1f} {'(Review)' if review else '(Auto)'}")
   
   return results

if __name__ == "__main__":
   process_all_forms()