import sys
import os
from mono_utils import process_pdf_form

def process_form(pdf_path, output_path, form_name="Medical Form"):
    """Process medical form PDF and save as JSON"""
    try:
        print(f"Extracting {form_name} Data...")
        result = process_pdf_form(pdf_path)
        
        with open(output_path, "w") as f:
            f.write(result if isinstance(result, str) else str(result))
        
        print(f"✓ {form_name} data extracted to: {output_path}")
        return True
    except Exception as e:
        print(f"Error processing {form_name}: {e}")
        return False

def main():
    """Command line interface for form processing."""
    if len(sys.argv) < 3:
        print("Usage: python form_processor.py <pdf_path> <output_path> [form_name]")
        print("Example: python form_processor.py ../data/pdf/CMS_Form.pdf ../outputs/cms_output.json 'CMS Form'")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_path = sys.argv[2]
    form_name = sys.argv[3] if len(sys.argv) > 3 else "Medical Form"
    
    success = process_form(pdf_path, output_path, form_name)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()