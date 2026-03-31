import pandas as pd
import matplotlib.pyplot as plt
import os

# ===== Load dataset safely =====
base_dir = os.path.dirname(os.path.dirname(__file__))
data_path = os.path.join(base_dir, "data", "cleaned_student_dataset.csv")

df = pd.read_csv(data_path)

print("Dataset shape:", df.shape)

# ===== Create output folder =====
output_dir = os.path.join(base_dir, "static")
os.makedirs(output_dir, exist_ok=True)

# ===== 1. Histogram =====
plt.figure()
plt.hist(df["exam_score"], bins=20)
plt.title("Distribution of Exam Scores")
plt.xlabel("Exam Score")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "histogram.png"))
plt.close()

# ===== 2. Study Hours vs Exam Score =====
plt.figure()
plt.scatter(df["study_hours"], df["exam_score"])
plt.title("Study Hours vs Exam Score")
plt.xlabel("Study Hours")
plt.ylabel("Exam Score")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "study_vs_score.png"))
plt.close()

# ===== 3. Gender vs Exam Score =====
plt.figure()
df.boxplot(column="exam_score", by="gender")
plt.title("Exam Score by Gender")
plt.suptitle("")
plt.xlabel("Gender")
plt.ylabel("Exam Score")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "gender_boxplot.png"))
plt.close()

# ===== 4. Correlation Heatmap =====
plt.figure()
corr = df.corr(numeric_only=True)
plt.imshow(corr, cmap="coolwarm")
plt.colorbar()
plt.xticks(range(len(corr)), corr.columns, rotation=90)
plt.yticks(range(len(corr)), corr.columns)
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "heatmap.png"))
plt.close()

# ===== 5. Academic Level vs Exam Score =====
plt.figure()
df.boxplot(column="exam_score", by="academic_level")
plt.title("Exam Score by Academic Level")
plt.suptitle("")
plt.xlabel("Academic Level")
plt.ylabel("Exam Score")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "academic_boxplot.png"))
plt.close()

# ===== 6. Sleep Hours vs Exam Score =====
plt.figure()
plt.scatter(df["sleep_hours"], df["exam_score"])
plt.title("Sleep Hours vs Exam Score")
plt.xlabel("Sleep Hours")
plt.ylabel("Exam Score")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "sleep_vs_score.png"))
plt.close()

print("✅ All visualizations saved in 'static/' folder")