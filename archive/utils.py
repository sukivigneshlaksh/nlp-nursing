import pickle
from pathlib import Path
import json

# Cache related
def save_parsed_doc(parsed_doc, pdf_path):
    cache_dir = Path("cache")
    cache_dir.mkdir(exist_ok=True)
    pdf_name = Path(pdf_path).stem
    cache_file = cache_dir / f"{pdf_name}_parsed.pkl"
    with open(cache_file, 'wb') as f:
        pickle.dump(parsed_doc, f)

def load_parsed_doc(pdf_path):
    pdf_name = Path(pdf_path).stem
    cache_file = Path("cache") / f"{pdf_name}_parsed.pkl"
    if cache_file.exists():
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    return None


# Conversion
def save_chunk_text(pkl_path: str, output_path: str = None):
    # Load pickle
    with open(pkl_path, 'rb') as f:
        data = pickle.load(f)
    
    # Default output path
    if output_path is None:
        output_path = Path(pkl_path).with_suffix('.json')
    
    cleaned = []
    for i, chunk in enumerate(data.chunks):
        cleaned_chunk = {
            "index": i + 1,
            "type": chunk.chunk_type.value,
            "text": chunk.text,
            "page": chunk.grounding[0].page if chunk.grounding else None,
            "chunk_id" : chunk.chunk_id
        }
        
        cleaned.append(cleaned_chunk)

    # Save as JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"Saved: {output_path}")
    return data
