import json
import os
import argparse
from mono_utils import load_json, generate_with_ai

def generate_conversation(form_structure):
    """Generate medical conversation based on form structure"""
    prompt = f"""Looking at this medical form structure, create a medical transcript that would include information needed to fill out the form fields.

    Form structure: {json.dumps(form_structure, indent=2)}

    Make the transcript a conversation between PATIENT and NURSE in the following style:
    **NURSE:** 
    **PATIENT:**
    **NURSE:**

    DO NOT INCLUDE ANYTHING EXCEPT THE NURSE, PATIENT CONVERSATION.
    """

    return generate_with_ai(prompt)

def main():
    parser = argparse.ArgumentParser(description='Generate sample transcript from form JSON')
    parser.add_argument('form_path', help='Path to the form JSON file')
    parser.add_argument('--output-dir', default='../outputs/sample_scripts', help='Output directory')
    
    args = parser.parse_args()
    
    # Load form JSON
    form_json = load_json(args.form_path)
    
    # Generate output filename
    base_name = os.path.splitext(os.path.basename(args.form_path))[0]
    output_file = os.path.join(args.output_dir, f"{base_name}_sample_transcript.txt")
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Generate conversation
    print(f"Generating transcript...")
    conversation = generate_conversation(form_json)
    
    # Save transcript
    with open(output_file, "w") as f:
        f.write(conversation)
    
    print(f"Transcript saved to: {output_file}")

if __name__ == "__main__":
    main()