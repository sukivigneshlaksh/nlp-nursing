from agentic_doc.parse import parse_documents
from agentic_doc.utils import viz_parsed_document
import json
import os

# Parse document
results = parse_documents(["pdf/Simple_Form.pdf"])
parsed_doc = results[0]

# Create output directory
os.makedirs("outputs_2", exist_ok=True)

# Create visual annotation
print("Creating visual annotation...")
images = viz_parsed_document(
    "pdf/Simple_Form.pdf",
    parsed_doc,
    output_dir="outputs_2/visualizations"
)

# Clean text output (no HTML comments)
import re
clean_text = re.sub(r'<!--.*?-->', '', parsed_doc.markdown).strip()

# Save clean text
with open("outputs_2/clean_text.txt", "w") as f:
    f.write(clean_text)

# Save chunks for further processing with grounding images
results_with_groundings = parse_documents(["pdf/CMS_Form.pdf"], grounding_save_dir="outputs_2/groundings")
parsed_doc_with_groundings = results_with_groundings[0]

chunks_data = []
for chunk in parsed_doc_with_groundings.chunks:
    chunk_data = {
        "text": chunk.text,
        "chunk_id": chunk.chunk_id,
        "image_paths": []
    }
    
    # Add grounding image paths if they exist
    for grounding in chunk.grounding:
        if grounding.image_path:
            chunk_data["image_paths"].append(str(grounding.image_path))
    
    chunks_data.append(chunk_data)

with open("outputs_2/chunks.json", "w") as f:
    json.dump(chunks_data, f, indent=2)

print("Saved to outputs_2/:")
print("  clean_text.txt - Clean markdown text")
print("  chunks.json - Text chunks with image paths for API processing")
print("  visualizations/ - Annotated images")
print("  groundings/ - Individual chunk images")