import pandas as pd
from radon.complexity import cc_visit
from radon.metrics import mi_visit
from radon.raw import analyze as raw_analyze

df = pd.read_csv("/Users/chaitanyaattanti/Downloads/lab_2/bug_fix_diffs_llm.csv")

print(df.columns)
def get_code_metrics(code):
    if pd.isna(code) or not isinstance(code, str) or code.strip() == "":
        return None, None, None
    try:
        # Maintainability Index
        mi_value = mi_visit(code, True)
        # Cyclomatic Complexity: average of all blocks
        cc_blocks = cc_visit(code)
        cc_value = sum(block.complexity for block in cc_blocks) / len(cc_blocks) if cc_blocks else 0
        # Lines of Code
        raw_stats = raw_analyze(code)
        loc_value = raw_stats.loc
        return mi_value, cc_value, loc_value
    except Exception:
        return None, None, None

#Compute metrics for Before code
df[['MI_Before', 'CC_Before', 'LOC_Before']] = df['Source Before'].apply(
    lambda x: pd.Series(get_code_metrics(x))
)

#Compute metrics for After code
df[['MI_After', 'CC_After', 'LOC_After']] = df['Source After'].apply(
    lambda x: pd.Series(get_code_metrics(x))
)

#Compute changes
df['MI_Change']  = df['MI_After'] - df['MI_Before']
df['CC_Change']  = df['CC_After'] - df['CC_Before']
df['LOC_Change'] = df['LOC_After'] - df['LOC_Before']

#Save enriched dataset
df.to_csv("bug_fix_commits_with_metrics.csv", index=False)
print("Metrics successfully computed and saved to bug_fix_commits_with_metrics.csv")
print(df.head())