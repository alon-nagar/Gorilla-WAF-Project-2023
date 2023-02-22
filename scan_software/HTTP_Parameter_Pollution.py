def is_request_hpp(request_data, args):
    """
        Function to check if a request contains HTTP Parameter Pollution (HPP) queries.
        
        Args:
            request_data (str): A JSON string of the request data [For example: {"username": "admin", "password": "<script>alert(1);</script>"}].
            args (ImmutableMultiDict): The query parameters to check.
        
        Returns:
            tuple(bool, str): A tuple of (True/False - HPP detected, str - The string where HPP was detected).
        
    """
    
    is_url_safe = is_url_hpp(args)
    if is_url_safe != (False, None):
        return is_url_safe
    
    for param_name, param_value in request_data.items():
        if is_text_hpp(param_value, args) != (False, None):
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
    print (text)
    for key, value in args.items():
        print (key)
        if ("&" + key + "=") in text:
            return (True, f"HTTP Parameter Pollution detected in param: {text})")
        
    return (False, None)




def is_url_hpp(args):
    """
    Check if the given args contains HTTP Parameter Pollution (HPP) queries.

    Args:
        args (ImmutableMultiDict): The query parameters to check.

    Returns:
        tuple: A tuple of (bool - True if HPP detected, str - The parameter name with HPP, or None if not detected).
    """
    param_names = []
    param_values = []
    for name, value in args.items():
        param_names.append(name)
        param_values.extend(value.split(","))

    if len(param_values) > len(set(param_names)):
        for name in param_names:
            if param_values.count(name) > 1:
                return (True, name)
        return (True, param_names[0])
    else:
        return (False, None)