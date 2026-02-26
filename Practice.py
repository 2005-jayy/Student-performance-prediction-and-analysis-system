import pandas as pd
import sklearn
from sklearn.linear_model import LogisticRegression

df=pd.read_csv("student_marks.csv")
print(df.head())
X=df[["Hours"]]
y=df["Pass/Fail"]
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model = LogisticRegression()
model.fit(X_train, y_train)
print("Prediction\n")
y_pred = model.predict(X_test)
print(y_pred)
print("Check Accuracy\n")
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, y_pred)
print(cm)

from sklearn.metrics import classification_report

print(classification_report(y_test, y_pred))

               
