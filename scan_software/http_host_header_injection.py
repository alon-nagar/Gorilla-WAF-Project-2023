import re

MAX_LEN = 1

def is_request_http_host_header(headers):
    """
    Function to check if a request contains a Host header injection attack.
    """
    # Check for the Host header and headers with similar purposes
    header_names = ['Host', 'X-Forwarded-Host', 'X-Host', 'X-Forwarded-Server', 'X-HTTP-Host-Override', 'Forwarded']
    for header_name in header_names:
        header_values = headers.getlist(header_name)
        
        # Check for duplicates
        if len(header_values) > MAX_LEN:
            return (True, header_name)
        
        for header_value in header_values:
            # Validate the header value
            if not re.match(r'^[a-zA-Z0-9.\-:]+$', header_value):
                return (True, header_name)
            
            # Check for host header injection attacks
            if any(keyword in header_value.lower() for keyword in ['\r', '\n', '%0d', '%0a']):
                return (True, header_name)
    return (False, None)
