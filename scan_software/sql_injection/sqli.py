"""
This script is used to detect SQLi (SQL Injection) queries from a given JSON string.
It uses a machine learning model that was trained in "sqli_train_model.py" at "ml_sqli_model.pickle".

Note: For this script to run correctly, you must first run "sqli_train_model.py" to train the model.

Requirements:
- pip install pickle
- pip install scikit-learn
"""


import pickle
from sklearn.feature_extraction.text import CountVectorizer


sqli_detection_model = pickle.load(open("ml_sqli_model.pickle", "rb"))
vectorizer = CountVectorizer()


def is_request_sqli(request_data):
    """Function to check if a request contains SQLi (SQL Injection) queries.

    Args:
        request_data (str): A JSON string of the request data [For example: {"username": "admin", "password": "' or 1=1--"}].

    Returns:
        tuple(bool, str): A tuple of (True/False - SQLi detected, str - The string where SQLi was detected).
    """
    
    for param_name, param_value in request_data.items():
        if is_text_sqli(param_value):
            return (True, param_value)
    
    return (False, None)
        
    
def is_text_sqli(text):
    """Function to check if a string contains SQLi (SQL Injection) queries.

    Args:
        text (str): The string to check if contains SQLi queries.

    Returns:
        bool: True - SQLi detected, False - Safe string.
    """
    return sqli_detection_model.predict(vectorizer.transform([text]))[0] == 1
