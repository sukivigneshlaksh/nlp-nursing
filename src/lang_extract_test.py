import textwrap
import langextract as lx
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('LANGEXTRACT_API_KEY')

# 1. Define a concise prompt
prompt = textwrap.dedent("""\
Extract characters, emotions, and relationships in order of appearance.
Use exact text for extractions. Do not paraphrase or overlap entities.
Provide meaningful attributes for each entity to add context.""")

# 2. Provide a high-quality example to guide the model
examples = [
    lx.data.ExampleData(
        text=(
            "ROMEO. But soft! What light through yonder window breaks? It is"
            " the east, and Juliet is the sun."
        ),
        extractions=[
            lx.data.Extraction(
                extraction_class="character",
                extraction_text="ROMEO",
                attributes={"emotional_state": "wonder"},
            ),
            lx.data.Extraction(
                extraction_class="emotion",
                extraction_text="But soft!",
                attributes={"feeling": "gentle awe"},
            ),
            lx.data.Extraction(
                extraction_class="relationship",
                extraction_text="Juliet is the sun",
                attributes={"type": "metaphor"},
            )
        ],
    )
]

# 3. Run the extraction on your input text
input_text = (
    "Lady Juliet gazed longingly at the stars, her heart aching for Romeo"
)
result = lx.extract(
    text_or_documents=input_text,
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-pro",
    api_key=api_key
)

# Print the extracted data
print(f"Input text: {input_text}\n")
print("Extracted entities:")
for extraction in result.extractions:
    print(f"  {extraction.extraction_class}: '{extraction.extraction_text}'")
    print(f"    Attributes: {extraction.attributes}")
    if hasattr(extraction, 'char_start') and hasattr(extraction, 'char_end'):
        print(f"    Position: {extraction.char_start}-{extraction.char_end}")
    print()
