from urllib.parse import urlparse, parse_qs

def is_request_open_redirect(url):
    """
        Function to check if a request contains an open redirect attack.
        Args:
            url (str): The URL of the request.
        Returns:
            tuple: (True, redirect_url) if the request contains an open redirect attack, (False, None) otherwise.
    """
    # Parse the URL to get the base URL and query parameters
    base_url = urlparse(url).scheme + "://" + urlparse(url).netloc + urlparse(url).path
    
    # Parse the query parameters
    query_params = parse_qs(urlparse(url).query)
    
    # Check for common redirect parameter names
    redirect_params = ["url", "target", "destination", "redir"]
    for param in redirect_params:
        if param in query_params:
            
            # Get the redirect URL
            redirect_url = query_params[param][0]
            
            # Check if the redirect URL is valid
            if redirect_url.startswith("http") and not redirect_url.startswith(base_url):
                return (True, redirect_url)
    
    return (False, None)
