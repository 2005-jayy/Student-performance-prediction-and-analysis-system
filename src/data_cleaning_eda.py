import pandas as pd
df=pd.read_csv("data/Student_Performance_datasetRaw.csv")

print(df.shape)

print(df.info())

print(df.describe())

print(df.isnull().sum())

print(df.duplicated().sum())
df=df.drop(['student_id'],axis=1)
#--------------------------------------No nulls values to fill------------------------------------------------

print("\nCategorical Columns:\n") #Sepaates Categorical columns from dataset
cateCol=df.select_dtypes(include='object').columns
print(cateCol)

print("\nNumeric Columns:\n") #Separates Numeric Columns from dataset
numCol=df.select_dtypes(exclude='object').columns
print(numCol)

#Correlation to identiffy positive and negative relationship between numeric features and exam_score
correlation=df.corr(numeric_only=True)['exam_score'].drop('exam_score')
correlation=correlation.sort_index(ascending=False)
print(correlation)
#5 Positive correlation
print("\n\n\nTop 5 positive correlation:")
positive_corr=correlation.nlargest(5)
print(positive_corr)
#5 negative correlation
print("\n\n\nTop 5 negative correlation:")
negative_corr=correlation.nsmallest(5)
print(negative_corr)


#Result Columns PASS/FAIL
print("Result")
df["result"] = (df["exam_score"] >= 40).astype(int)

#Grade Column
def grade(score):
    if score >= 75:
        return "A"
    elif score >= 60:
        return "B"
    elif score >= 40:
        return "C"
    else:
        return "Fail"

df["grade"] = df["exam_score"].apply(grade)
print(df[['exam_score','result','grade']].head())

#Clean data csv
df.to_csv("data/cleaned_student_dataset.csv", index=False)