from urllib.parse import urlparse, parse_qs

def is_request_open_redirect(url):
    # Parse the URL to get the base URL and query parameters
    base_url = urlparse(url).scheme + "://" + urlparse(url).netloc + urlparse(url).path
    query_params = parse_qs(urlparse(url).query)
    
    # Check for common redirect parameter names
    redirect_params = ["url", "target", "destination", "redir"]
    for param in redirect_params:
        if param in query_params:
            redirect_url = query_params[param][0]
            if redirect_url.startswith("http") and not redirect_url.startswith(base_url):
                return (True, redirect_url)
    
    return (False, None)
