import json
import sys
from mono_utils import generate_with_ai

def chunk_ideas(sentences):
    """Split sentences into idea chunks"""
    text = "\n".join([f"{i+1}. {s}" for i, s in enumerate(sentences)])
    
    prompt = f"""Group these sentences by idea. Return as array of arrays with the actual sentences.

{text}

Return: [["sentence1", "sentence2"], ["sentence3", "sentence4"]]"""
    
    response = generate_with_ai(prompt)
    try:
        return json.loads(response)
    except:
        return [sentences]

def main():
    if len(sys.argv) < 2:
        print("Usage: python idea_chunker.py \"sent1\" \"sent2\" \"sent3\" \"sent4\"")
        return
    
    sentences = sys.argv[1:]
    chunks = chunk_ideas(sentences)
    
    print("Idea chunks:")
    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i}:")
        for sentence in chunk:
            print(f"  • {sentence}")

if __name__ == "__main__":
    main()