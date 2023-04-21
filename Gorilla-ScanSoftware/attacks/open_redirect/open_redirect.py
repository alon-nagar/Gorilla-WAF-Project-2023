import re
from urllib.parse import urlparse, parse_qs, unquote
 
    
def is_request_open_redirect(db, request_data):
    """Function to check if a request contains an open redirect attack.
    
    Args:
        url (str): The URL of the request.
        allowed_domains (list of str): A list of allowed domains. If None, any domain is allowed.
    
    Returns:
        tuple: (True, url_to_enter) if the request contains an open redirect attack, (False, None) otherwise.
    """
    allowed_urls = db.get_all_allowed_urls()
    
    # Check for common redirect parameter names
    redirect_params = ["url", "uri", "path", "next", "go", "data", "view", "page", "location", "return", "redir", "redirect", "redirect_uri", "redirect_url"]
    
    # Check if one of the requet's parameters is redirect parameter:
    for redirect_param in redirect_params:
        if redirect_param in request_data.keys():
            
            # Check if url to enter is from allowed urls: 
            url_to_enter = request_data[redirect_param]
            if url_to_enter not in allowed_urls:
                return (True, f"{redirect_param}={url_to_enter}")
            
    return (False, None)
