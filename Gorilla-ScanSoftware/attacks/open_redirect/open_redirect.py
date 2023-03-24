import re
from urllib.parse import urlparse, parse_qs, unquote


def allowed_redirection_urls():
    """
    Function to get a list of allowed redirection URLs from the file "allowed_redirection_urls.txt".
    
    Args:
        None.
        
    Returns:
        list: A list of allowed redirection URLs.
    """
    allowed_redirection_urls = []
    
    # Open the file "allowed_redirection_urls.txt" and read each line to the list:
    with open("../Gorilla-ScanSoftware/attacks/open_redirect/allowed_redirection_urls.txt", "r") as f:
        for line in f:
            allowed_redirection_urls.append(line.strip())
    
    return allowed_redirection_urls
            
    
def is_request_open_redirect(request_data, allowed_domains=None):
    """Function to check if a request contains an open redirect attack.
    
    Args:
        url (str): The URL of the request.
        allowed_domains (list of str): A list of allowed domains. If None, any domain is allowed.
    
    Returns:
        tuple: (True, url_to_enter) if the request contains an open redirect attack, (False, None) otherwise.
    """
    allowed_urls = allowed_redirection_urls()
    
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
