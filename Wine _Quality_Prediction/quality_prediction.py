# -*- coding: utf-8 -*-
"""Quality_Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LSub_EKhghVStMEZd203o8gXvliSJRzP
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE
from scipy import stats
from scipy import special

data_frame=pd.read_csv('/content/drive/MyDrive/Certificates/Internship/Offer Letters/Internship/TechnoHack/wine.zip')

data_frame

data_frame.shape

data_frame.describe()

data_frame.isnull().sum()

print("Is there any Duplicate Records => ",data_frame.duplicated().any())
print("-"*42)
print("Total Duplicate Records present is =>",data_frame[data_frame.duplicated()==True].shape[0])

data_frame.drop_duplicates(inplace=True)

data_frame.describe()

plt.figure(figsize=(9,6))
z = data_frame["quality"].value_counts()
sns.barplot(x=z.index, y=z.values, order=z.index)
plt.title("Target Feature Distributions",fontweight="black",size=25,pad=15)
for index,value in enumerate(z.values):
    plt.text(index,value,value, ha="center", va="bottom",fontweight="black")

plt.tight_layout()
plt.show()

data_frame["quality"].unique()

#Condition of Splitting: If quality > 6.5 => "good" ELSE => "bad"

bin_edges = [0,6.5,10]
group_names = ["Bad","Good"]

data_frame["quality"] = pd.cut(data_frame["quality"], bins=bin_edges, labels=group_names)
data_frame["quality"].unique()

plt.figure(figsize=(10,6))
plt.subplot(1,2,1)
quality_counts = data_frame["quality"].value_counts()
sns.barplot(x=quality_counts.index, y=quality_counts.values)
plt.title("Wine Quality Value Counts",fontweight="black",size=20,pad=20)
for i, v in enumerate(quality_counts.values):
    plt.text(i, v, v,ha="center", fontweight='black', fontsize=18)

plt.subplot(1,2,2)
plt.pie(quality_counts, labels=["Bad","Good"], autopct="%.2f%%", textprops={"fontweight":"black","size":15},
        colors = ["#1d7874","#AC1F29"],explode=[0,0.1],startangle=90)
center_circle = plt.Circle((0, 0), 0.3, fc='white')
fig = plt.gcf()
fig.gca().add_artist(center_circle)
plt.title("Wine Quality Values Distrbution" ,fontweight="black",size=20,pad=10)
plt.show()

data_frame["quality"] = data_frame["quality"].replace({"Bad":0,"Good":1})

data_frame.sample(5)

new_df  = data_frame.copy()
columns = data_frame.columns.tolist()
columns.remove("quality")

skew_df = data_frame[columns].skew().to_frame().rename(columns={0:"Skewness"})
skew_df

columns = data_frame.columns.tolist()
columns.remove("quality")
skewness_transformation = {}

for col in columns:
    transformed_log = np.log(data_frame[col])                        # Log Transformation
    transformed_boxcox = special.boxcox1p(data_frame[col], 0.15)     # Box-Cox Transformation with lambda=0.15
    transformed_inverse = 1 / data_frame[col]                        # Inverse Transformation
    transformed_yeojohnson, _ = stats.yeojohnson(data_frame[col])    # Yeo-Johnson Transformation
    transformed_cbrt = np.cbrt(data_frame[col])                      # Cube Root Transformation

    # Create a dictionary for the skewness values of each transformation
    transformation_skewness = {
        "Log Transformation": stats.skew(transformed_log),
        "Box-Cox Transformation": stats.skew(transformed_boxcox),
        "Inverse Transformation": stats.skew(transformed_inverse),
        "Yeo Johnson Transformation": stats.skew(transformed_yeojohnson),
        "Cube Root Transformation": stats.skew(transformed_cbrt)}

    # Store the transformation skewness values for the column
    skewness_transformation[col] = transformation_skewness

result_df = pd.DataFrame.from_dict(skewness_transformation, orient='index')
result_df = pd.concat([skew_df["Skewness"], result_df], axis=1)
result_df

for col in columns:
    transformed_col,_ = stats.yeojohnson(data_frame[col])
    data_frame[col] = transformed_col

data_frame.sample(5)

x=1
y=2


plt.figure(figsize=(25,60))
for col in columns:
    plt.subplot(11,2,x)
    sns.histplot(new_df[col],kde=True,color="purple")
    plt.title(f"Distribution of {col} Before Transformation",fontweight="black",size=25,pad=10)
    x+=2

    plt.subplot(11,2,y)
    sns.histplot(data_frame[col],kde=True, color="orange")
    plt.title(f"Distribution of {col} After Transformation",fontweight="black",size=25,pad=10)
    y+=2

    plt.tight_layout()

X = data_frame.drop('quality', axis=1)
y = data_frame['quality']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train.shape

y_train.shape

# Apply SMOTE to balance the classes in the training set
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

# Choose a model (Random Forest Classifier)
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model on the resampled training data
model.fit(X_train_resampled, y_train_resampled)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate model performance
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')

print("F1 Score of the Model is =>",f1_score(y_test,y_test_pred, average="weighted"))
print("Recall Score of the Model is =>",recall_score(y_test,y_test_pred, average="weighted"))
print("Precision Score of the Model is =>",precision_score(y_test,y_test_pred, average="weighted"))

imp_df = pd.DataFrame({"Feature Name":x_train.columns,
                       "Importance":dtree.feature_importances_})

features = imp_df.sort_values(by="Importance",ascending=False)

plt.figure(figsize=(12,7))
sns.barplot(x="Importance", y="Feature Name", data=features, palette="plasma")
plt.title("Feature Importance in the Model Prediction", fontweight="black", size=20, pad=20)
plt.yticks(size=12)
plt.show()

