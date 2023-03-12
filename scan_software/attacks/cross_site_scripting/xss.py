xss_keywords_list = []

with open("attacks/cross_site_scripting/xss_keywords.txt", "r") as xss_keywords_file:
    xss_keywords_list = xss_keywords_file.read().splitlines()  # Read each line and append it to the liss (without the '\n' character).
    
def is_request_xss(request_data):
    """Function to check if a request contains XSS (Cross-Site Scripting) characters.

    Args:
        request_data (str): A JSON string of the request data [For example: {"username": "admin", "password": "<script>alert(1);</script>"}].

    Returns:
        tuple(bool, str): A tuple of (True/False - XSS detected, str - The string where XSS was detected).
    """
    
    for param_name, param_value in request_data.items():
        if is_text_xss(param_value):
            return (True, param_value)
    
    return (False, None)
        
    
def is_text_xss(text):
    """Function to check if a string contains XSS (Cross-Site Scripting) characters.

    Args:
        text (str): The string to check if contains XSS characters.

    Returns:
        bool: True - XSS detected, False - Safe string.
    """
    text = text.replace(" ", "").replace("\n", "").replace("\t", "")  # Remove all spaces, new lines and tabs.
    text = text.lower()                                               # Convert the string to lower case.
    
    # If the text to check contains one of the XSS keywords (from the 'xss_keywords_list'), return True:
    return any(xss_keyword in text for xss_keyword in xss_keywords_list)
