"""
This script is used to train a machine learning model to detect SQLi from a given CSV file.
Then, it exports the model to a file called "ml_sqli_model.pickle" for later use in the actual WAF scanner [in "sqli.py"].

Note: Run this script before running "sqli.py" to train the model.

Requirements:
- pip install pandas
- pip install scikit-learn
- pip install pickle
"""


import pandas as pd  # For data and CSV file handling.

# Import general ML libraries:
from sklearn.feature_extraction.text import CountVectorizer  # For vectorization (converting text data into numerical features).
from sklearn.metrics import accuracy_score                   # For calculating accuracy of model.
from sklearn.model_selection import train_test_split         # For splitting data into training and testing sets.

# Import models:
from sklearn.linear_model import LogisticRegression  # For Logistic Regression model.
from sklearn.naive_bayes import MultinomialNB        # For Naive Bayes model.
from sklearn.svm import LinearSVC                    # For Support Vector Machine model.

# Export/Import model [dump/load]:
import pickle


# Read CSV file into Pandas DataFrame:
data = pd.read_csv("Modified_SQL_Dataset.csv")  # Source: https://www.kaggle.com/datasets/sajid576/sql-injection-dataset

# Extract Queries and Labels: 0 = Not SQL, 1 = SQLi.
queries = data["Query"].tolist()
labels = data["Label"].tolist()

# Convert text data into numerical features ("vectorization"):
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(queries)

"""
-------------------[ This is how we test which model is the best ]-------------------

# Split data into training and testing sets:
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2)

# Define models to test:
models = [ MultinomialNB(), LogisticRegression(), LinearSVC() ]
models_names = [ "Naive Bayes", "Logistic Regression", "Support Vector Machine" ]

# Test each model:
for model, model_name in zip(models, models_names):
    # Train model:
    model.fit(X_train, y_train)

    # Test model:
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"{model_name}".ljust(27) + f"{accuracy}")
"""

model = LinearSVC()   # Define the best model [Support Vector Machine].
model.fit(X, labels)  # Train model

# Export model&vectorizer to a file called "ml_sqli_model.pickle" and "vectorizer_ml_sqli_model.pickle":
pickle.dump(model, open("ml_sqli_model.pickle", "wb"))
pickle.dump(vectorizer, open("vectorizer_ml_sqli_model.pickle", "wb"))
