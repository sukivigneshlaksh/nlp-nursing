import argparse
from pathlib import Path
from agent.extraction_agent import PDFExtractionAgent
from agent.verification_agent import VisionVerificationAgent
'''
llm generates form structure for a specific form

and then that's passed as a pydantic model

look at github form

Use small form and do entire form -> one api call with correct pydantic request
'''


def main():
    parser = argparse.ArgumentParser(description="Process PDF forms with extraction, verification, and form filling")
    
    # Main input arguments
    parser.add_argument("pdf_path", nargs='?', help="Path to the PDF file to process")
    
    # Mode selection
    parser.add_argument("--extract-only", action="store_true", 
                       help="Only run extraction, skip verification")
    parser.add_argument("--verify-only", action="store_true",
                       help="Only run verification (requires existing extraction)")
    parser.add_argument("--fill-only", action="store_true",
                       help="Only run form filling (requires existing extraction and transcript)")
    
    # Form filling specific arguments
    parser.add_argument("--transcript", type=str,
                       help="Path to transcript file for form filling")
    parser.add_argument("--json-input", type=str,
                       help="Path to existing JSON file for form filling (for --fill-only mode)")
    
    # Configuration arguments
    parser.add_argument("--output-dir", default="outputs",
                       help="Output directory for results")
    parser.add_argument("--extraction-model", default="openai:o4-mini",
                       help="Model for extraction agent (e.g., 'vertex:gemini-1.5-flash', 'openai:gpt-4o-mini')")
    parser.add_argument("--vision-model", default="gemini-1.5-flash",
                       help="Model for vision verification agent (e.g., 'gemini-1.5-flash', 'openai:gpt-4o')")
    parser.add_argument("--project-id", default="suki-dev",
                       help="GCP project ID for Vertex AI")
    parser.add_argument("--location", default="us-central1",
                       help="GCP location for Vertex AI")
    
    args = parser.parse_args()
    
    # Validate arguments based on mode
    if args.fill_only:
        if not args.json_input or not args.transcript:
            print("Error: --fill-only mode requires both --json-input and --transcript arguments")
            return 1
        
        if not Path(args.json_input).exists():
            print(f"Error: JSON input file not found: {args.json_input}")
            return 1
            
        if not Path(args.transcript).exists():
            print(f"Error: Transcript file not found: {args.transcript}")
            return 1
    else:
        if not args.pdf_path:
            print("Error: PDF path is required unless using --fill-only mode")
            return 1
            
        # Validate PDF file
        pdf_path = Path(args.pdf_path)
        if not pdf_path.exists():
            print(f"Error: PDF file not found: {pdf_path}")
            return 1
        
        args.pdf_path = str(pdf_path)
    
    try:
        # Handle fill-only mode
        if args.fill_only:
            print("Starting form filling...")
            print(f"JSON input: {args.json_input}")
            print(f"Transcript: {args.transcript}")
            print(f"Using extraction model: {args.extraction_model}")
            
            extraction_agent = PDFExtractionAgent(
                model=args.extraction_model,
                output_dir=args.output_dir,
                project_id=args.project_id,
                location=args.location
            )
            
            filled_results = extraction_agent.fill_form_fields(args.json_input, args.transcript)
            print("Form filling complete!")
            return 0
        
        # Run extraction 
        if not args.verify_only:
            print("Starting PDF form extraction...")
            print(f"Using extraction model: {args.extraction_model}")
            
            extraction_agent = PDFExtractionAgent(
                model=args.extraction_model,
                output_dir=args.output_dir,
                project_id=args.project_id,
                location=args.location
            )
            extraction_results = extraction_agent.process(args.pdf_path)
            
            # If transcript provided, automatically run form filling after extraction
            if args.transcript:
                print(f"\nTranscript provided: {args.transcript}")
                print("Running form filling after extraction...")
                
                # Get the path to the generated JSON file
                pdf_name = Path(args.pdf_path).stem
                json_path = f"{args.output_dir}/2-text_to_json_initial/{pdf_name}_simple.json"
                
                if Path(json_path).exists():
                    filled_results = extraction_agent.fill_form_fields(json_path, args.transcript)
                else:
                    print(f"Warning: Could not find extraction output at {json_path}")
            
            if args.extract_only:
                print("Extraction complete!")
                return 0
        
        # Run verification 
        if not args.extract_only:
            print("Starting vision verification...")
            print(f"Using vision model: {args.vision_model}")
            print(f"Project: {args.project_id}, Location: {args.location}")
            
            verification_agent = VisionVerificationAgent(
                model=args.vision_model,
                output_dir=args.output_dir,
                project_id=args.project_id,
                location=args.location
            )
            verification_results = verification_agent.process(args.pdf_path)
            
            # If transcript provided and we didn't already fill in extraction phase
            if args.transcript and args.verify_only:
                print(f"\nTranscript provided: {args.transcript}")
                print("Running form filling after verification...")
                
                # Create extraction agent for form filling
                extraction_agent = PDFExtractionAgent(
                    model=args.extraction_model,
                    output_dir=args.output_dir,
                    project_id=args.project_id,
                    location=args.location
                )
                
                # Try to find the best JSON file (verification output first, then extraction)
                pdf_name = Path(args.pdf_path).stem
                json_candidates = [
                    f"{args.output_dir}/3-text_to_json_verified/{pdf_name}_verified.json",
                    f"{args.output_dir}/2-text_to_json_initial/{pdf_name}_simple.json",
                    f"{args.output_dir}/2-text_to_json_initial/{pdf_name}.json"
                ]
                
                json_path = None
                for candidate in json_candidates:
                    if Path(candidate).exists():
                        json_path = candidate
                        break
                
                if json_path:
                    filled_results = extraction_agent.fill_form_fields(json_path, args.transcript)
                else:
                    print("Warning: Could not find JSON file for form filling")
        
        print("Vision processing complete!")
        return 0
        
    except Exception as e:
        print(f"Error during processing: {e}")
        import traceback
        traceback.print_exc()
        return 1


def run_full_pipeline(pdf_path: str, output_dir: str = "outputs", 
                     extraction_model: str = "openai:o4-mini",
                     vision_model: str = "gemini-1.5-flash",
                     project_id: str = "suki-dev",
                     location: str = "us-central1",
                     transcript_path: str = None):
    """
    Run the complete pipeline including optional form filling
    """
    print(f"Starting full pipeline for: {pdf_path}")
    print(f"Extraction model: {extraction_model}")
    print(f"Vision model: {vision_model}")
    print(f"Vertex AI project: {project_id}, location: {location}")
    if transcript_path:
        print(f"Transcript for form filling: {transcript_path}")
    
    extraction_agent = PDFExtractionAgent(
        model=extraction_model, 
        output_dir=output_dir,
        project_id=project_id,
        location=location
    )
    verification_agent = VisionVerificationAgent(
        model=vision_model, 
        output_dir=output_dir,
        project_id=project_id,
        location=location
    )
    
    print("Running extraction...")
    extraction_results = extraction_agent.process(pdf_path)
    
    print("Running verification...")
    verification_results = verification_agent.process(pdf_path)
    
    filled_results = None
    if transcript_path:
        print("Running form filling...")
        # Use verification output if available, otherwise extraction output
        pdf_name = Path(pdf_path).stem
        json_candidates = [
            f"{output_dir}/3-text_to_json_verified/{pdf_name}_verified.json",
            f"{output_dir}/2-text_to_json_initial/{pdf_name}_simple.json"
        ]
        
        json_path = None
        for candidate in json_candidates:
            if Path(candidate).exists():
                json_path = candidate
                break
        
        if json_path:
            filled_results = extraction_agent.fill_form_fields(json_path, transcript_path)
        else:
            print("Warning: Could not find JSON file for form filling")
    
    print("Pipeline complete")
    return extraction_results, verification_results, filled_results


def run_extraction_only(pdf_path: str, output_dir: str = "outputs", 
                       model: str = "openai:o4-mini",
                       project_id: str = "suki-dev",
                       location: str = "us-central1",
                       transcript_path: str = None):
    """
    Run extraction only, with optional form filling
    """
    print(f"Running extraction for: {pdf_path}")
    print(f"Using model: {model}")
    if transcript_path:
        print(f"Transcript for form filling: {transcript_path}")
    
    extraction_agent = PDFExtractionAgent(
        model=model, 
        output_dir=output_dir,
        project_id=project_id,
        location=location
    )
    extraction_results = extraction_agent.process(pdf_path)
    
    filled_results = None
    if transcript_path:
        print("Running form filling...")
        pdf_name = Path(pdf_path).stem
        json_path = f"{output_dir}/2-text_to_json_initial/{pdf_name}_simple.json"
        
        if Path(json_path).exists():
            filled_results = extraction_agent.fill_form_fields(json_path, transcript_path)
        else:
            print(f"Warning: Could not find extraction output at {json_path}")
    
    print("Extraction complete")
    return extraction_results, filled_results


def run_verification_only(pdf_path: str, output_dir: str = "outputs",
                         model: str = "gemini-1.5-flash",
                         project_id: str = "suki-dev",
                         location: str = "us-central1"):
    """
    Run verification only
    """
    print(f"Running verification for: {pdf_path}")
    print(f"Using model: {model}")
    print(f"Vertex AI project: {project_id}, location: {location}")
    
    verification_agent = VisionVerificationAgent(
        model=model, 
        output_dir=output_dir,
        project_id=project_id,
        location=location
    )
    results = verification_agent.process(pdf_path)
    
    print("Verification complete!")
    return results


def run_form_filling_only(json_path: str, transcript_path: str, 
                         output_dir: str = "outputs",
                         model: str = "openai:o4-mini",
                         project_id: str = "suki-dev",
                         location: str = "us-central1"):
    """
    Run form filling only using existing JSON and transcript
    """
    print(f"Running form filling...")
    print(f"JSON input: {json_path}")
    print(f"Transcript: {transcript_path}")
    print(f"Using model: {model}")
    
    extraction_agent = PDFExtractionAgent(
        model=model,
        output_dir=output_dir,
        project_id=project_id,
        location=location
    )
    
    results = extraction_agent.fill_form_fields(json_path, transcript_path)
    
    print("Form filling complete!")
    return results


if __name__ == "__main__":
    exit(main())