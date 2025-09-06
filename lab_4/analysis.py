import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load CSV
df = pd.read_csv("diff_data_added_discrepancy.csv")

# For classifying file types (focusing on the 4 required categories)
def classify_file(filepath):
    if pd.isna(filepath):
        return "Other"
    
    filepath = str(filepath).lower()
    
    if "test" in filepath:
        return "Test Code"
    elif "readme" in filepath:
        return "README"
    elif "license" in filepath:
        return "LICENSE"
    elif filepath.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.c', '.rb', '.go', '.cs', '.php')):
        return "Source Code"
    else:
        return "Other"

# Apply classification
df["file_type"] = df["old_file_path"].apply(classify_file)

# Calculate statistics for the 4 required categories
required_types = ["Source Code", "Test Code", "README", "LICENSE"]
results = {}

for file_type in required_types:
    type_files = df[df["file_type"] == file_type]
    total_count = len(type_files)
    mismatch_count = len(type_files[type_files["discrepancy"] == "Yes"])
    mismatch_rate = (mismatch_count / total_count * 100) if total_count > 0 else 0
    
    results[file_type] = {
        "Total Files": total_count,
        "Mismatches": mismatch_count,
        "Matches": total_count - mismatch_count,
        "Mismatch Rate (%)": mismatch_rate
    }

# Convert to DataFrame for easy display
stats_df = pd.DataFrame(results).T

print("="*60)
print("  REPORT")
print("="*60)
print("Mismatch Analysis by File Type:")
print(stats_df.round(3))
print()

print("📈 Requested Statistics:")
for file_type in required_types:
    count = results[file_type]["Mismatches"]
    total = results[file_type]["Total Files"]
    rate = results[file_type]["Mismatch Rate (%)"]
    print(f"• #Mismatches for {file_type} files: {count} out of {total} ({rate:.1f}%)")

# Create visualizations
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

ax1, ax2, ax3, ax4, ax5, ax6 = axes.flatten()

# 1. Bar chart of mismatch counts
mismatch_counts = [results[ft]["Mismatches"] for ft in required_types]
bars1 = ax1.bar(required_types, mismatch_counts, color=['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4'])
ax1.set_title("Number of Mismatches by File Type", fontweight='bold', fontsize=14)
ax1.set_ylabel("Number of Mismatches")
ax1.tick_params(axis='x', rotation=45)
ax1.grid(axis='y', alpha=0.3)

# Add value labels
for bar, count in zip(bars1, mismatch_counts):
    if count > 0:
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                str(count), ha='center', va='bottom', fontweight='bold')

# 2. Mismatch rates bar chart
mismatch_rates = [results[ft]["Mismatch Rate (%)"] for ft in required_types]
bars2 = ax2.bar(required_types, mismatch_rates, color=['#ff8a80', '#80cbc4', '#81c784', '#ffb74d'])
ax2.set_title("Mismatch Rate by File Type", fontweight='bold', fontsize=14)
ax2.set_ylabel("Mismatch Rate (%)")
ax2.tick_params(axis='x', rotation=45)
ax2.grid(axis='y', alpha=0.3)

# Add value labels
for bar, rate in zip(bars2, mismatch_rates):
    if rate > 0:
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')

# 3-6. Pie charts for each file type (Matches vs Mismatches)
pie_axes = [ax3, ax4, ax5, ax6]
colors = ['lightgreen', 'lightcoral']

for ax, ft in zip(pie_axes, required_types):
    matches = results[ft]["Matches"]
    mismatches = results[ft]["Mismatches"]
    ax.pie([matches, mismatches],
           labels=["Matches", "Mismatches"],
           autopct='%1.1f%%',
           startangle=90,
           colors=colors)
    ax.set_title(f"{ft}: Matches vs Mismatches", fontweight='bold', fontsize=12)

plt.tight_layout()
plt.show()

# Overall summary
total_files_analyzed = sum(results[ft]["Total Files"] for ft in required_types)
total_mismatches_found = sum(results[ft]["Mismatches"] for ft in required_types)
overall_mismatch_rate = (total_mismatches_found / total_files_analyzed * 100) if total_files_analyzed > 0 else 0

print("\n" + "="*60)
print("📋 FINAL SUMMARY")
print("="*60)
print(f"Total Files Analyzed: {total_files_analyzed:,}")
print(f"Total Mismatches Found: {total_mismatches_found:,}")
print(f"Overall Mismatch Rate: {overall_mismatch_rate:.2f}%")
print()
print("File Type Breakdown:")
for file_type in required_types:
    data = results[file_type]
    print(f"  {file_type:<12}: {data['Mismatches']:>4} mismatches / {data['Total Files']:>5} total ({data['Mismatch Rate (%)']:>5.1f}%)")
