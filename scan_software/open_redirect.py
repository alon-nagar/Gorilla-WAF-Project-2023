import re
from urllib.parse import urlparse, parse_qs, unquote

def is_request_open_redirect(url, allowed_domains=None):
    """
    Function to check if a request contains an open redirect attack.
    Args:
        url (str): The URL of the request.
        allowed_domains (list of str): A list of allowed domains. If None, any domain is allowed.
    Returns:
        tuple: (True, redirect_url) if the request contains an open redirect attack, (False, None) otherwise.
    """

    # Parse the URL to get the base URL and query parameters
    parsed_url = urlparse(url)
    base_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path

    # Parse the query parameters
    query_params = parse_qs(parsed_url.query, keep_blank_values=True)

    # Check for common redirect parameter names
    redirect_params = ["url", "uri", "path", "next", "go", "data", "view", "page", "location", "return", "redir", "redirect", "redirect_uri", "redirect_url"]
    
    for param in redirect_params:
        if param in query_params:
            redirect_url = query_params[param][0]

            # Check if the redirect URL is valid
            if re.match(r"^https?://", redirect_url):

                # Check if the redirect URL is in the list of allowed domains
                if allowed_domains is None or urlparse(redirect_url).hostname in allowed_domains:
                    return (True, redirect_url)
                
            elif redirect_url.startswith("/"):

                # Construct the full redirect URL
                redirect_url = parsed_url.scheme + "://" + parsed_url.netloc + redirect_url

                # Check if the redirect URL is in the list of allowed domains
                if allowed_domains is None or urlparse(redirect_url).hostname in allowed_domains:
                    return (True, redirect_url)
                
            else:
                try:
                    # Check for URL encoding
                    redirect_url = unquote(redirect_url)
                    redirect_url = unquote(redirect_url) # Double unquote in case the URL is encoded more then once

                    # Check if the redirect URL is valid
                    if re.match(r"^https?://", redirect_url):

                        # Check if the redirect URL is in the list of allowed domains
                        if allowed_domains is None or urlparse(redirect_url).hostname in allowed_domains:
                            return (True, redirect_url)
                    elif redirect_url.startswith("/"):

                        # Construct the full redirect URL
                        redirect_url = parsed_url.scheme + "://" + parsed_url.netloc + redirect_url

                        # Check if the redirect URL is in the list of allowed domains
                        if allowed_domains is None or urlparse(redirect_url).hostname in allowed_domains:
                            return (True, redirect_url)
                except:
                    pass

    return (False, None)
