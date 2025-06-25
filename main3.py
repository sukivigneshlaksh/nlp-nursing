import openai
import os
from dotenv import load_dotenv
import json
from form_files.simple_form import MedicalHistoryForm, sample_transcript, MEDICAL_HISTORY_CLINICAL_WEIGHTS

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

def evaluate_extraction_with_weights(extracted_data, transcript):
   """Evaluate extraction quality with clinical weights"""
   field_evaluations = {}
   weighted_total = 0
   weight_sum = 0
   
   # Get data as dict
   data_dict = extracted_data.model_dump()
   
   # Evaluate each top-level field
   for field_name, field_value in data_dict.items():
       if field_value is None:
           continue
           
       # Get clinical weight
       weight = MEDICAL_HISTORY_CLINICAL_WEIGHTS.get(field_name, 1.0)
       
       # Evaluate field
       score = evaluate_field(field_name, field_value, transcript)
       weighted_score = score * weight
       
       field_evaluations[field_name] = {
           "score": score,
           "weight": weight,
           "weighted_score": weighted_score,
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

def process_medical_history():
   """Process medical history form with weighted evaluation"""
   
   # Extract data
   extracted_data = extract_medical_data(sample_transcript, MedicalHistoryForm)
   
   # Evaluate with weights
   evaluation = evaluate_extraction_with_weights(extracted_data, sample_transcript)
   
   # Combine results
   result = {
       "form_type": "Medical History",
       "extracted_data": extracted_data.model_dump(),
       "evaluation": evaluation
   }
   
   # Save to JSON
   with open("medical_history_weighted_results.json", "w") as f:
       json.dump(result, f, indent=2)
   
   print(f"Overall Score: {evaluation['overall_weighted_score']}")
   print(f"Review Recommended: {evaluation['review_recommended']}")
   
   return result

if __name__ == "__main__":
   process_medical_history()