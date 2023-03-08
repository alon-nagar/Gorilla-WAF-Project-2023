def is_request_hpp(request_data, url):
    """
        Function to check if a request contains HTTP Parameter Pollution (HPP).
          First, it checks for HPP in the parameters when entered in the URL directly.
          Then, it checks for HPP in the parameters when entered in a input field.
        
        Args:
            request_data (str): A JSON string of the request data [For example: {"username": "admin", "password": "<script>alert(1);</script>"}].
            args (ImmutableMultiDict): The query parameters to check.
        
        Returns:
            tuple(bool, str): A tuple of (True/False - HPP detected, str - The string where HPP was detected).
        
    """
    
    is_url_safe = is_url_hpp(url)
    if is_url_safe != (False, None):
        return is_url_safe
    
    for param_name, param_value in request_data.items():
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

    for key, value in args.items():
        print (key)
        if ("&" + key + "=") in text:
            return (True, f"HTTP Parameter Pollution detected in param: {text})")

    return (False, None)




def is_url_hpp(url):
    """
    Check if the given URL contains HTTP Parameter Pollution (HPP) queries.

    Args:
        url (str): The URL to check.

    Returns:
        tuple: A tuple of (bool - True if HPP detected, str - The parameter name with HPP, or None if not detected).
    """
    url_parts = url.split("?")
    if len(url_parts) < 2:
        return (False, None)

    params = url_parts[1].split("&")
    param_dict = {}
    hpp_param = None
    for p in params:
        if "=" not in p:
            continue
        name, value = p.split("=")
        if name in param_dict:
            param_dict[name].append(value)
        else:
            param_dict[name] = [value]

        if len(param_dict[name]) > 1 or any("%2C" in v for v in param_dict[name]):
            hpp_param = name
            break

    return (True if hpp_param else False, hpp_param)