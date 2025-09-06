from pydriller import Repository
import pandas as pd
import git


git.refresh(path='/usr/bin/git')  

repo = "https://github.com/microsoft/vscode-python"

bug_fix_commits = []

keywords = [
    "fixed", "bug", "fixes", "fix", "crash", "solves", "resolves", "issue", "regression",
    "fall back", "assertion", "coverity", "reproducible", "stack-wanted", "steps-wanted",
    "testcase", "failure", "fail", "npe", "except", "broken", "differential testing",
    "error", "hang", "test fix", "steps to reproduce", "leak", "stack trace",
    "heap overflow", "freez", "problem", "overflow", "avoid", "workaround", "break", "stop"
]



for commit in Repository(repo).traverse_commits():
    msg = commit.msg.lower()
    if any(keyword in msg.lower() for keyword in keywords):
        bug_fix_commits.append({
            'Hash': commit.hash,
            'Message': commit.msg,
            'Hashes of parents': commit.parents,  
            'Is a merge commit?': commit.merge,
            'List of modified files': [f.filename for f in commit.modified_files]
    })

df_commits = pd.DataFrame(bug_fix_commits)
df_commits.to_csv('bug_fix_commits.csv', index=False)
print("Saving Done ")

