import json

def is_xss(request_data):
    """Function to check if a request contains XSS (Cross-Site Scripting) characters.

    Args:
        request_data (str): A JSON string of the request data [For example: {"username": "admin", "password": "<script>alert(1);</script>"}].

    Returns:
        tuple(bool, str): A tuple of (True/False - XSS detected, str - The string where XSS was detected).
    """
    #data_json = json.loads(request_data)
    
    print(request_data)#
    for param_name, param_value in request_data.items():
        if is_text_xss(param_value):
            return (True, param_value)
    
    print("No XSS detected!")#
    return (False, None)
        
    
def is_text_xss(text):
    """Function to check if a string contains XSS (Cross-Site Scripting) characters.

    Args:
        text (str): The string to check if contains XSS characters.

    Returns:
        bool: True - XSS detected, False - Safe string.
    """
    return any(danger_char in text.lower() for danger_char in ["<", ">", "&lt;", "&gt;"])
