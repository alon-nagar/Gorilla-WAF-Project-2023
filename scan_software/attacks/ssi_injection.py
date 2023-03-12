import re  # Regular expressions (RegEx) library.

regex_ssii_rule = re.compile("<!--#(.*?)-->")  # Regular expression to match SSIi (Server-Side Includes Injection) characters.

def is_request_ssi_injection(request_data):
    """Function to check if a request contains SSIi (Server-Side Includes Injection) characters.

    Args:
        request_data (str): A JSON string of the request data [For example: {"username": "admin", "password": "<!--#exec cmd=”whoami”-->"}].

    Returns:
        tuple(bool, str): A tuple of (True/False - SSIi detected, str - The string where SSIi was detected).
    """
    
    for param_name, param_value in request_data.items():
        if is_text_ssii(param_value):
            return (True, param_value)
    
    return (False, None)
        
    
def is_text_ssii(text):
    """Function to check if a string contains XSS SSIi (Server-Side Includes Injection) characters.

    Args:
        text (str): The string to check if contains SSIi characters.

    Returns:
        bool: True - SSIi detected, False - Safe string.
    """
    return regex_ssii_rule.match(text)
