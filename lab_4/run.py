import csv
import subprocess
from pydriller import Repository

repositories = [
    "/Users/chaitanyaattanti/Downloads/lab_4/codeception",
    "/Users/chaitanyaattanti/Downloads/lab_4/httprunner",
    "/Users/chaitanyaattanti/Downloads/lab_4/open_spiel"
]

output_file = "diff_data.csv"

def extract_diff(repo_path, par_commit, cur_commit, target_file, algorithm):
    command = [
        "git", "-C", repo_path, "diff",
        f"--diff-algorithm={algorithm}",
        "-w", "--ignore-blank-lines",
        par_commit, cur_commit, "--", target_file
    ]
    res = subprocess.run(command, capture_output=True, text=True)
    return res.stdout.strip()

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow([
        "old_file_path", "new_file_path",
        "commit_SHA", "parent_commit_SHA",
        "commit_message", "diff_myers", "diff_hist"
    ])
    
    for path in repositories:
        print(f"\nProcessing repo: {path}")
        for cur_commit in Repository(path).traverse_commits():
            if len(cur_commit.parents) != 1:
                continue
            parent_commit_sha = cur_commit.parents[0]
            
            for modification in cur_commit.modified_files:
                old_file_path = modification.old_path or ""
                new_file_path = modification.new_path or ""
                target_file_path = new_file_path if new_file_path else old_file_path
                
                try:
                    myers_diff = extract_diff(path, parent_commit_sha, cur_commit.hash, target_file_path, "myers")
                    histogram_diff = extract_diff(path, parent_commit_sha, cur_commit.hash, target_file_path, "histogram")
                    
                    csv_writer.writerow([
                        old_file_path, new_file_path,
                        cur_commit.hash, parent_commit_sha,
                        cur_commit.msg.strip().replace("\n", " "),
                        myers_diff, histogram_diff
                    ])
                except Exception as error:
                    print("Error processing")