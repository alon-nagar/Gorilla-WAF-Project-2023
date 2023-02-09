import urllib
from urllib.parse import urlparse, parse_qs

def is_request_hpp(request_data, url):
    """
        Function to check if a request contains HTTP Parameter Pollution (HPP) queries.
        
        Args:
            request_data (str): A JSON string of the request data [For example: {"username": "admin", "password": "<script>alert(1);</script>"}].
            url (str): The URL of the request.
        
        Returns:
            tuple(bool, str): A tuple of (True/False - HPP detected, str - The string where HPP was detected).
        
    """
    for param_name, param_value in request_data.items():
        if is_text_hpp(param_value, url) != (False, None):
            return (True, param_value)
        
    return (False, None)


def is_text_hpp(text, url):
    """
        Function to check if a string contains HTTP Parameter Pollution (HPP) queries.
        
        Args:
            text (str): The string to check if contains HPP queries.
            url (str): The URL of the request.
        
        Returns:
            tuple(bool, str): A tuple of (True/False - HPP detected, str - The string where HPP was detected).
    """
    query_params = extract_query_params(url)
    if "=" in text:
        field = text[:text.index("=")]
        field = field.strip()
        if (field in query_params):
            return (True, f"HTTP Parameter Pollution detected in param: {text}")
        
    return (False, None)


def extract_query_params (url):
    """ 
        Function to extract the query parameters from a URL.
        
        For example: https://www.example.com/?param1=value1&param2=value2
        will return: {'param1': ['value1'], 'param2': ['value2']}
        
        Args:
        url (str): The URL to extract the query parameters from.
        
        Returns:
        query_params (dict): A dictionary of the query parameters.
        
    """
    parsed_url = urlparse(url)
    query_string = parsed_url.query
    query_params = parse_qs(query_string)
    return query_params