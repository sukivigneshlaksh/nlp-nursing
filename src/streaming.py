import os
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')
#model = SentenceTransformer('pritamdeka/S-PubMedBert-MS-MARCO')

# lower threshold to bias things towards prev dialogue
PREV_THRESHOLD = 0.4
REFERENCE_BACK_THRESHOLD = 0.6

# new algo thresholds
THRESHOLD = 0.5
BIAS = 0.025

def parse_interactions(text):
    """Parse transcript into pairs of nurse-patient interactions"""
    interactions = []
    lines = text.strip().split('\n')
    clean_lines = []
    
    # First, get all clean lines with nurse/patient interactions
    for line in lines:
        clean_line = line.strip()
        if clean_line and ('**NURSE:**' in clean_line or '**PATIENT:**' in clean_line or 'PATIENT:' in clean_line or 'NURSE:' in clean_line):
            clean_lines.append(clean_line)
    
    # Group pairs of lines together representing one interaction
    for i in range(0, len(clean_lines), 2):
        if i + 1 < len(clean_lines):
            pair = clean_lines[i] + " " + clean_lines[i + 1]
            interactions.append(pair)
    
    return interactions


def load_cms_script():
    script_path = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'sample_scripts', 'disjoint_stress_transcript.txt')
    with open(script_path, 'r') as f:
        text = f.read()
    return parse_interactions(text)


def get_disjoint_dialogues(sentences):
    if not sentences:
        return []
    
    dialogues = [[sentences[0]]]
    dialogue_embeddings = [model.encode(sentences[0])]  # Single sentence, not array

    for i in range(1, len(sentences)):
        curr_sentence = sentences[i]
        curr_emb = model.encode(curr_sentence)  # Single sentence embedding

        best_sim, best_idx = -1, None
        
        for j, prev_embedding in enumerate(dialogue_embeddings):
            sim = cosine_similarity([curr_emb], [prev_embedding])[0][0]

            # bias towards prev dialogue
            if j == len(dialogue_embeddings) - 1:
                sim += BIAS

            if sim > best_sim:
                best_sim, best_idx = sim, j
        
        if best_sim > THRESHOLD:
            if best_idx != len(dialogue_embeddings) - 1:
                # to denote reference back case
                dialogues[best_idx].append('...\n')
                dialogues[best_idx].append(curr_sentence)
                string = ''.join(dialogues[best_idx])

                dialogue_embeddings[best_idx] = model.encode(string)
            else:
                # if last dialogue
                dialogues[best_idx].append(curr_sentence)
                dialogue_embeddings[best_idx] = model.encode(''.join(dialogues[best_idx]))
        else:
            dialogues.append([curr_sentence])
            dialogue_embeddings.append(model.encode(curr_sentence))
    
    return dialogues

def construct_string(ir):
    pass

def create_ir_semantics(ir):
    '''Iterate through given ir; create and place semantics'''
    # iterate through information
    pass

def get_ir_semantics(dialogue_semantics, ir):
    '''Get semantically similar parts of ir structure to given dialogue'''
    pass

def main():
    interactions = load_cms_script()
    dialogues = get_disjoint_dialogues(interactions)
    
    for i, dialogue in enumerate(dialogues):
        print(f"Dialogue {i+1}:")
        for interaction in dialogue:
            if interaction == "...":
                print("-")
            else:
                print(f"  {interaction}")
        print("\n\n")
    
    
    

    



if __name__ == "__main__":
    main()