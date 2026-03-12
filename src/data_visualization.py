import pandas as pd 
import matplotlib.pyplot as plt

df = pd.read_csv("data/cleaned_student_dataset.csv")

print(df.shape)

#let's start the visulization of cleaned data set 

#here we are plot the histogram for the distributions of marks and using 20 bins cause we have is data for visulization

plt.hist(df["Marks"], bins=20, edgecolor="blue")
plt.title("Distribution of marks of students")
plt.xlabel("Marks")
plt.ylabel("freq")
plt.show()


#now let's lets plot the graph to identify relation between studyhours and marks of students
plt.scatter(df["StudyHours"], df["Marks"], color="orange")
plt.title("Study hrs vs marks")
plt.xlabel("study hrs")
plt.ylabel("marks obtained")
plt.show()

#now we will see the comparison of marks on bases of gender
plt.boxplot(df["Marks"]by= df["gender"])
plt.title("comparison of marks on bases of gender")
plt.xlabel("gender")
plt.ylabel("Marks obtained")
plt.show()


#now the  time for the corelation heatmap to identify the corelation between numeric features in our data set
plt.figure()
corr = df.corr(numeric_only=True)
plt.imshow(corr)
plt.colorbar()
plt.xticks(range(len(corr)), corr.columns, rotation=90)
plt.yticks(range(len(corr)),corr.columns)
plt.title("heatmap")
plt.show()