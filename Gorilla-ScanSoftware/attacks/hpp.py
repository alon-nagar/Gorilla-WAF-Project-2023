import urllib.parse


def is_request_hpp(request_url):
    """
    Function that checks if a request contains HTTP Parameter Pollution (HPP).
        First, it checks for HPP in the parameters when entered in the URL directly [/?name=a,b].
        Then, it checks for HPP in the parameters when entered in a input field [?name=a%26name%3Db] (%26=&, %3D==).
    
    Args:
        request_data (str): A JSON string of the request data.
        args (ImmutableMultiDict): The query parameters to check.
    
    Returns:
        tuple(bool, str): A tuple of (True/False - HPP detected, str - The string where HPP was detected)
    """
    
    # Parse the URL:
    parsed_url = urllib.parse.urlparse(request_url)
    
    # Get the parameters as a dictionary
    params_dict = urllib.parse.parse_qs(parsed_url.query)
    
    # Check if any parameter has more than one value:
    for param_name, param_values in params_dict.items():
        if len(param_values) > 1:
            return (True, f"{param_name}={param_values}")

    return (False, None)
