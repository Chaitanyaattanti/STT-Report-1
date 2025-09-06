import csv
import re
import pandas as pd
import matplotlib.pyplot as plt

in_file = "/Users/chaitanyaattanti/Downloads/lab_2/bug_fix_diffs_llm.csv"

keywords = [
    "fixed", "bug", "fixes", "fix", "crash", "solves", "resolves", "issue", "regression",
    "fall back", "assertion", "coverity", "reproducible", "stack-wanted", "steps-wanted",
    "testcase", "failure", "fail", "npe", "except", "broken", "differential testing",
    "error", "hang", "test fix", "steps to reproduce", "leak", "stack trace",
    "heap overflow", "freez", "problem", "overflow", "avoid", "workaround", "break", "stop"
]

def is_precise(msg, fname=None, thresh=2):  # relaxed threshold
    if not msg or not isinstance(msg, str):
        return False
    msg_low = msg.lower()
    score = 0

    # filename presence
    if fname and fname.lower() in msg_low:
        score += 1

    # action words anywhere (not just start)
    if re.search(r"\b(add|fix|update|remove)\b", msg_low):
        score += 1

    # count ALL keyword matches
    score += sum(1 for k in keywords if k in msg_low)

    # special case boost
    if "bug fix" in msg_low or "fix bug" in msg_low:
        score += 1

    # technical terms
    if re.search(r"\.py|\.cpp|function|method|class|error|crash|exception|leak", msg_low):
        score += 2

    return score >= thresh

# --- Load data ---
df = pd.read_csv(in_file)

# --- Adding precision labels ---
df["Dev_Precise"] = df["Developer Message"].apply(is_precise)
df["LLM_Precise"] = df["LLM Inference"].apply(is_precise)
df["Rect_Precise"] = df["Rectified Message"].apply(is_precise)

# --- Hit rates ---
total = len(df)
dev_precise = df["Dev_Precise"].sum()
llm_precise = df["LLM_Precise"].sum()
rect_precise = df["Rect_Precise"].sum()

hit_rates = {
    "Developer": round(dev_precise / total * 100, 3),
    "LLM": round(llm_precise / total * 100, 3),
    "Rectifier": round(rect_precise / total * 100, 3),
}

print("  Hit Rates (RQ1–RQ3) ")
for k, v in hit_rates.items():
    print(f"{k}: {v}% precise")

# Save updated dataframe
df.to_csv("bug_fixes_eval.csv", index=False)

# --- Plot ---
plt.bar(hit_rates.keys(), hit_rates.values())
plt.ylabel("Hit Rate (%)")
plt.title("Commit Message Precision Comparison")
plt.show()
