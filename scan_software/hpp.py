def is_request_hpp(request_data, url):
    """
        Function that checks if a request contains HTTP Parameter Pollution (HPP).
          First, it checks for HPP in the parameters when entered in the URL directly.
          Then, it checks for HPP in the parameters when entered in a input field.
        
        Args:
            request_data (str): A JSON string of the request data.
            args (ImmutableMultiDict): The query parameters to check.
        
        Returns:
            tuple(bool, str): A tuple of (True/False - HPP detected, str - The string where HPP was detected).
        
    """
    
    # Send the request URL to the function that checks it.
    is_url_safe = is_url_hpp(url)
    
    # Check if the URL is safe.
    if is_url_safe != (False, None):
        return is_url_safe
    
    # Check if the request data contains HPP.
    for param_name, param_value in request_data.items():
        # Send the request data to the function that checks it.
        if is_text_hpp(param_value, request_data) != (False, None):
            return (True, param_name)
        
    return (False, None)


def is_text_hpp(text, args):
    """
        Function to check if a string contains HTTP Parameter Pollution (HPP) queries.
        
        Args:
            text (str): The string to check if contains HPP queries.
            args (ImmutableMultiDict): The query parameters to check.        
        Returns:
            tuple(bool, str): A tuple of (True/False - HPP detected, str - The string where HPP was detected).
    """
    # Loop through all the keys and values in the query parameters.
    for key, value in args.items():
        # Check if the parameter key is present in the text.
        if ("&" + key + "=") in text:
            # Return a tuple indicating that HPP was detected and the parameter name with HPP.
            return (True, f"{text}")

    return (False, None)


def is_url_hpp(url):
    """
    Check if the given URL contains HTTP Parameter Pollution (HPP) queries.

    Args:
        url (str): The URL to check.

    Returns:
        tuple: A tuple of (bool - True if HPP detected, str - The parameter name with HPP, or None if not detected).
    """
    
    # Split the URL into two parts: the part before the query string and the part after.
    url_parts = url.split("?")
    
    # If the URL has no query string, return False and None.
    if len(url_parts) < 2:
        return (False, None)

    # Split the query string into individual parameters.
    query_string = url_parts[1]
    params = query_string.split("&")
    
    # Create an empty dictionary to hold the parameters.
    param_dict = {}
    hpp_param = None
    
    for p in params:

        # If the parameter doesn't contain an equals sign, skip it meaning that it can't be a parameter.
        if "=" not in p:
            continue
        
        # Split the parameter into its name and value.
        name, value = p.split("=")
        
        # If the parameter is already in the dictionary, append the value to its list.
        # Otherwise, add the parameter and its value to the dictionary.
        if name in param_dict:
            param_dict[name].append(value)
        else:
            param_dict[name] = [value]
            
        # If the parameter appears more than once or contains the string "%2C",
        # it may indicate HPP, so set the HPP parameter to the current name and break the loop.
        if len(param_dict[name]) > 1 or any("%2C" in v for v in param_dict[name]):
            hpp_param = name
            break
        
    # Return True and the name of the HPP parameter if one was found, or False and None otherwise.
    return (True if hpp_param else False, hpp_param)