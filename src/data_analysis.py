import pandas as pd
df=pd.read_csv("data/cleaned_student_dataset.csv")

print("Exam Score Statistics:")
print(df["exam_score"].describe())

avg_score = df["exam_score"].mean()
print(f"\nAverage Exam Score: {avg_score:.2f}\n")

print("========== CORRELATION ANALYSIS ==========\n")
correlation=df.corr(numeric_only=True)['exam_score'].drop('exam_score')
correlation=correlation.sort_index(ascending=False)
#top 5 Positive correlation
print("\n\n\nTop 5 positive correlation:")
positive_corr=correlation.nlargest(5)
print(positive_corr)
#top 5 negative correlation
print("\n\n\nTop 5 negative correlation:")
negative_corr=correlation.nsmallest(5)
print(negative_corr)

print("\nInsights:")
print("Features with higher positive correlation tend to increase exam performance.")
print("Features with negative correlation may reduce academic performance.\n")

print("\n")
print("========== GENDER ANALYSIS ==========\n")
gender_score=df.groupby("gender")["exam_score"].mean()
print(gender_score)
diff=gender_score.max()-gender_score.min()
if diff <1:
      print('\nInsight: gender has minimal influence on exam score.\n')
else:
      top_gender=gender_score.idxmax()
      print(f"\n Insights: {top_gender} students perform sightly better on average.\n")

#Academic level Analysis
print("========== ACADEMIC LEVEL ANALYSIS ==========\n")
level_scores=df.groupby("academic_level")["exam_score"].mean()
print(level_scores)
diff = level_scores.max() - level_scores.min()

if diff < 1:
    print("\nInsight: Academic level shows minimal difference in exam performance.\n")
else:
    best = level_scores.idxmax()
    print(f"\nInsight: {best} students tend to perform better.\n")

#Intenret quality
print("===========INTERNET QUALITY ANALYSIS==========\n")
internet_scores=df.groupby("internet_quality")["exam_score"].mean()
print(internet_scores)

diff=internet_scores.max()-internet_scores.min()
if diff < 1:
    print("\nInsight: Internet quality does not significantly impact exam scores.\n")
else:
    best = internet_scores.idxmax()
    print(f"\nInsight: Students with {best} internet perform better.\n")


# Study Hours Impact
print("========== STUDY HOURS IMPACT ==========\n")

low_study = df[df["study_hours"] < 2]["exam_score"].mean()
high_study = df[df["study_hours"] > 6]["exam_score"].mean()

print("Average Score (Low Study Hours):", low_study)
print("Average Score (High Study Hours):", high_study)

if high_study > low_study:
    print("\nInsight: Students who study more hours tend to score higher.\n")
else:
    print("\nInsight: Study hours do not show a strong difference in performance.\n")



# Burnout Impact
print("========== BURNOUT IMPACT ==========\n")

low_burnout = df[df["burnout_level"] < 4]["exam_score"].mean()
high_burnout = df[df["burnout_level"] > 7]["exam_score"].mean()

print("Average Score (Low Burnout):", low_burnout)
print("Average Score (High Burnout):", high_burnout)

if high_burnout < low_burnout:
    print("\nInsight: Higher burnout levels are associated with lower exam scores.\n")
else:
    print("\nInsight: Burnout does not significantly affect performance in this dataset.\n")



# Final Analytical Summary
print("========== FINAL INSIGHTS ==========\n")

print("1. Behavioral factors such as study hours, productivity, and focus are likely strong predictors of exam performance.")
print("2. Burnout and excessive distractions may negatively impact student performance.")
print("3. Demographic factors like gender or academic level show minimal influence in this dataset.")
print("4. Academic success appears more dependent on student habits and productivity than demographic characteristics.")

print("\n========== END OF ANALYSIS ==========")