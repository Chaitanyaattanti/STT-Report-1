import pandas as pd
import matplotlib.pyplot as plt

# ---- Load dataset ----
df = pd.read_csv("bug_fix_commits_with_all_metrics.csv")

# ---- Drop NaN semantic similarity rows ----

token_values = df["Token_Similarity"].dropna()

# ---- Plot histogram ----
plt.figure(figsize=(10,6))
plt.hist(token_values, bins=20, color='skyblue', edgecolor='black')
plt.title("Distribution of Token Similarity (CodeBERT) for Bug-Fix Commits")
plt.xlabel("Token Similarity ")
plt.ylabel("Frequency (Number of Commits)")
plt.grid(axis='y', alpha=0.75)
plt.show()

Semantic_values=  df["Semantic_Similarity"].dropna()

# ---- Plot histogram ----
plt.figure(figsize=(10,6))
plt.hist(Semantic_values, bins=20, color='skyblue', edgecolor='black')
plt.title("Distribution of Semantic Similarity (CodeBERT) for Bug-Fix Commits")
plt.xlabel("Semantic  Similarity ")
plt.ylabel("Frequency (Number of Commits)")
plt.grid(axis='y', alpha=0.75)
plt.show()

