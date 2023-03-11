def is_request_xst(full_request):
    """
    Function to check if HTTP request contains Cross-Site Tracing (XST) attack.
    It simply done by checking if the request method is TRACE.

    Args:
        full_request (flask.request): The full Flask request to check.

    Returns:
        bool: True if the request contains XST attack, False otherwise.
    """
    
    return full_request.method == "TRACE"
