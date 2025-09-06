import pandas as pd

input_csv = "diff_data.csv"
output_csv = "diff_data_added_discrepancy.csv"

df = pd.read_csv(input_csv)

df["discrepancy"] = df.apply(
    lambda row: "No" if row["diff_myers"] == row["diff_hist"] else "Yes",
    axis=1
)

df.to_csv(output_csv, index=False)

print(f"Discrepancy column added and saved to {output_csv}")

