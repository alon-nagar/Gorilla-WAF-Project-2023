"""
This script is used to train a machine learning model to detect SQLi from a given CSV file.
Then, it exports the model to a file called "ml_sqli_model.pickle" for later use in the actual WAF scanner [in "sqli.py"].

Note: Run this script before running "sqli.py" to train the model.

Requirements:
- pip install pandas
- pip install scikit-learn
- pip install pickle
"""


from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
import warnings
warnings.filterwarnings('ignore')


# # For data and CSV file handling:
import pandas as pd

# # Import general ML libraries:
# from sklearn.feature_extraction.text import CountVectorizer  # For vectorization (converting text data into numerical features).
# from sklearn.metrics import accuracy_score                   # For calculating accuracy of model.
# from sklearn.model_selection import train_test_split         # For splitting data into training and testing sets.

# # Import models:
# from sklearn.linear_model import LogisticRegression  # For Logistic Regression model.
# from sklearn.naive_bayes import MultinomialNB        # For Naive Bayes model.
# from sklearn.svm import LinearSVC                    # For Support Vector Machine model.

# Export/Import model [dump/load]:
import pickle
import nltk

nltk.download('stopwords')

warnings.filterwarnings('ignore')  # Ignore warnings from sklearn.

# Read CSV file into Pandas DataFrame:
data = pd.read_csv("Modified_SQL_Dataset.csv")  # Source: https://www.kaggle.com/datasets/sajid576/sql-injection-dataset

# Extract Queries and Labels: 0 = Not SQL, 1 = SQLi.
queries = data["Query"]
labels = data["Label"]
from sklearn import tree

# Convert text data into numerical features ("vectorization"):
vectorizer = CountVectorizer(min_df = 2, max_df = 0.8, stop_words = stopwords.words('english'))
X = vectorizer.fit_transform(queries.astype('U')).toarray()

print(1)

model = tree.DecisionTreeClassifier()   # Define the best model [Support Vector Machine].
print(2)
model.fit(X, labels)  # Train model
print(3)
# Export model&vectorizer to a file called "ml_sqli_model.pickle" and "vectorizer_ml_sqli_model.pickle":
pickle.dump(model, open("ml_sqli_model.pickle", "wb"))
pickle.dump(vectorizer, open("vectorizer_ml_sqli_model.pickle", "wb"))
