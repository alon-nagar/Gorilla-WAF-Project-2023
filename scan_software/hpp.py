def is_request_hpp(request_data):
    """
        Function to check if a request contains HTTP Parameter Pollution (HPP) queries.
        
        Args:
            request_data (str): A JSON string of the request data [For example: {"username": "admin", "password": "<script>alert(1);</script>"}].
        
        Returns:
            tuple(bool, str): A tuple of (True/False - HPP detected, str - The string where HPP was detected).
        
    """
    for param_name, param_value in request_data.items():
        if is_text_hpp(param_value) != (False, None):
            return (True, param_value)
        
    return (False, None)


def is_text_hpp(text):
    """
        Function to check if a string contains HTTP Parameter Pollution (HPP) queries.
        
        Args:
            text (str): The string to check if contains HPP queries.
            url (str): The URL of the request.
        
        Returns:
            tuple(bool, str): A tuple of (True/False - HPP detected, str - The string where HPP was detected).
    """
    if "=" in text and "&" in text:
        return (True, f"HTTP Parameter Pollution detected in param: {text}")
        
    return (False, None)