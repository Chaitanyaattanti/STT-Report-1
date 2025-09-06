import csv
import re
from pydriller import Repository
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

repo = "https://github.com/microsoft/vscode-python"
output_csv = "bug_fix_diffs_llm.csv"

keywords = [
    "fixed", "bug", "fixes", "fix", "crash", "solves", "resolves", "issue", "regression",
    "fall back", "assertion", "coverity", "reproducible", "stack-wanted", "steps-wanted",
    "testcase", "failure", "fail", "npe", "except", "broken", "differential testing",
    "error", "hang", "test fix", "steps to reproduce", "leak", "stack trace",
    "heap overflow", "freez", "problem", "overflow", "avoid", "workaround", "break", "stop"
]


token = AutoTokenizer.from_pretrained("mamiksik/CommitPredictorT5")
model = AutoModelForSeq2SeqLM.from_pretrained("mamiksik/CommitPredictorT5")

def get_llm_msg(commit_msg, diff):
    input_text = f"Original message: {commit_msg}\nDiff:\n{diff}\nRectify:"
    inputs = token(input_text, return_tensors="pt", truncation=True, max_length=512)
    outputs = model.generate(**inputs, max_length=64)
    llm_msg = token.decode(outputs[0], skip_special_tokens=True)
    return llm_msg

def is_precise(msg, fname=None, thresh=2):
    if not msg:
        return False
    score = 0
    if fname and fname.lower() in msg.lower():
        score += 1
    if re.match(r"^(add|update|fix|remove)\b", msg.lower()):
        score += 1
    if any(k in msg.lower() for k in keywords):
        score += 1
    if re.search(r"\.py|\.cpp|\.h|function|method|class|error|crash|exception|leak", msg.lower()):
        score += 2

    return score >= thresh

def rect_msg(dev_msg, llm_msg, fname):
    dev_msg, llm_msg = dev_msg.strip(), (llm_msg.strip() if llm_msg else "")
    if is_precise(dev_msg):
        return dev_msg
    if llm_msg and llm_msg.lower() != "unknown":
        return llm_msg if fname in llm_msg else f"{llm_msg} in {fname}"
    return f"Bug fix in {fname}"

with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Hash",
        "Developer Message",
        "Filename",
        "Source Before",
        "Source After",
        "Diff",
        "LLM Inference",
        "Rectified Message"
    ])

    for commit in Repository(repo).traverse_commits():
        msg = commit.msg.strip()
        if any(keyword in msg.lower() for keyword in keywords):
            for mod in commit.modified_files:
                before_txt = mod.source_code_before.replace("\n", "\\n") if mod.source_code_before else ""
                after_txt = mod.source_code.replace("\n", "\\n") if mod.source_code else ""
                diff_txt = mod.diff.replace("\n", "\\n") if mod.diff else ""

                # LLM analysis and message refinement
                llm_msg = get_llm_msg(msg, diff_txt)

                rectified = rect_msg(msg, llm_msg, mod.filename)

                writer.writerow([
                    commit.hash,
                    msg,
                    mod.filename,
                    before_txt,
                    after_txt,
                    diff_txt,
                    llm_msg,
                    rectified
                ])
print(f"Bug fix diffs with LLM and Rectified messages are saved to {output_csv}")
print("Saving Done")
