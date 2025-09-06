import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

df = pd.read_csv("/Users/chaitanyaattanti/Downloads/lab3/bug_fix_commits_with_all_metrics.csv")

# Create Semantic and Token class columns
semantic_threshold = 0.995
token_threshold = 0.7

df["Semantic_Class"] = df["Semantic_Similarity"].apply(lambda x: "Minor" if x >= semantic_threshold else "Major")
df["Token_Class"] = df["Token_Similarity"].apply(lambda x: "Minor" if x >= token_threshold else "Major")

# Agreement column
df["Classes_Agree"] = df.apply(lambda row: "YES" if row["Semantic_Class"] == row["Token_Class"] else "NO", axis=1)

# Confusion matrix
y_true = df["Semantic_Class"]
y_pred = df["Token_Class"]

cm = confusion_matrix(y_true, y_pred, labels=["Minor","Major"])
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Minor","Major"])
disp.plot(cmap=plt.cm.Blues, values_format='d')
plt.title(f"Confusion Matrix (Token threshold = {token_threshold})")
plt.show()

agreement_percentage = (cm[0,0] + cm[1,1]) / cm.sum() * 100
print("Confusion Matrix:")
print(cm)
print(f"\nOverall agreement percentage: {agreement_percentage:.2f}%")