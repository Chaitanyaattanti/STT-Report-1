import pandas as pd
import os

# Load dataset
df = pd.read_csv("/Users/chaitanyaattanti/Downloads/lab_2/bug_fix_diffs_llm.csv")

# Basic statistics
commit_count = df["Hash"].nunique()
file_count = df["Filename"].nunique()
avg_files_per_commit = df.groupby("Hash")["Filename"].nunique().mean()

# Top 10 modified files
top_files = df["Filename"].value_counts().head(10)

# Top 10 file extensions (exclude empty)
df["Ext"] = df["Filename"].map(lambda f: os.path.splitext(str(f))[1])
top_exts = df["Ext"].value_counts()
top_exts = top_exts[top_exts.index != ''].head(10)

# Top 10 fix types
fix_types = df["LLM Inference"].value_counts().head(10)

# Print results
print("=== Descriptive Statistics ===")
print(f"Total commits: {commit_count}")
print(f"Unique files: {file_count}")
print(f"Average files per commit: {avg_files_per_commit:.2f}\n")

print("=== Top 10 Modified Files ===")
print(top_files, "\n")

print("=== Top 10 File Extensions ===")
print(top_exts, "\n")

print("=== Top 10 Fix Types ===")
print(fix_types)
