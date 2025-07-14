# NLP Nursing Form Processor

Agentic document processing for medical forms using Landing AI + Vertex AI.

## Setup

```bash
pip install agentic-doc vertexai python-dotenv PyMuPDF
export VISION_AGENT_API_KEY="your-api-key"
```

## Usage

```python
python src/agentic_doc_processor.py
```

Processes 4 medical forms with concurrent kernel processing:
- Simple Form
- CMS Form  
- UHC Form
- Wellness Form

## Output

Each PDF generates:
- `{form_name}_processed.json` - Complete analysis with form fields
- `{form_name}_chunks.pkl` - Cached document chunks

## Demo

```bash
streamlit run demo.py
```