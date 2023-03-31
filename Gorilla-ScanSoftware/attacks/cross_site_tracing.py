def is_request_xst(full_request):
    """
    Function to check if HTTP request contains Cross-Site Tracing (XST) attack.
    It simply done by checking if the request method is TRACE.

    Args:
        full_request (flask.request): The full Flask request to check.

    Returns:
        bool: True if the request contains XST attack, False otherwise.
        tuple(bool, str): A tuple of (True/False - XST detected, str - The string where XST was detected [first request's line]).

    """
    
    return (full_request.method == "TRACE", f"{full_request.method} {full_request.path} {full_request.environ['SERVER_PROTOCOL']}")
