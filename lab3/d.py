import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModel
import sacrebleu
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv("/Users/chaitanyaattanti/Downloads/lab_2/bug_fix_diffs_llm.csv")

# Load CodeBERT model
device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModel.from_pretrained("microsoft/codebert-base").to(device)

def embed(text):
    """Generate vector embedding for the given code using CodeBERT"""
    if not isinstance(text, str) or text.strip() == "":
        return None
    tokens = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=256).to(device)
    with torch.no_grad():
        output = model(**tokens)
    # Mean pooling over token embeddings
    return output.last_hidden_state.mean(1).cpu().numpy()

def semantic_similarity(a, b):
    """Compute cosine similarity between two code snippets"""
    try:
        emb1, emb2 = embed(a), embed(b)
        if emb1 is None or emb2 is None:
            return None
        sim = cosine_similarity(emb1, emb2)[0, 0]
        # Normalize to range 0–1
        return (sim + 1) / 2
    except:
        return None

def token_similarity(a, b):
    """Compute normalized BLEU score between two code snippets"""
    try:
        if not isinstance(a, str) or not isinstance(b, str):
            return None
        bleu = sacrebleu.sentence_bleu(b, [a]).score
        return bleu / 100.0
    except:
        return None

# Compute semantic and token similarity for each commit
df['Semantic_Similarity'] = df.apply(
    lambda r: semantic_similarity(str(r['Source Before']), str(r['Source After'])),
    axis=1
)
df['Token_Similarity'] = df.apply(
    lambda r: token_similarity(str(r['Source Before']), str(r['Source After'])),
    axis=1
)

# Save the results to a CSV file
df.to_csv("bug_fix_commits_with_all_metrics.csv", index=False)

print("Semantic_Similarity and Token_Similarity columns added")
print(df[['Filename','Semantic_Similarity','Token_Similarity']].head())
print("Results saved to bug_fix_commits_with_all_metrics.csv")