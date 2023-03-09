import re

def is_request_http_host_header(request_headers):
    """
    Function to check if a request contains a Host Header injection attack.
     HHI Attack occures when [Noa]
    
    Args:
        request_headers (werkzeug.datastructures.Headers): The HTTP request's headers.
        
    Returns:
        tuple: (True, "{header_name}: {header_val}"): A tuple of (True - HHI detected, str - The header name and value where HHI was detected).
    """
    
    # Define the headers to check (there are several headers that can be used to set the Host header):
    host_header_names = ['Host', 'X-Forwarded-Host', 'X-Host', 'X-Forwarded-Server', 'X-HTTP-Host-Override', 'Forwarded']
    
    # For each header name, get all the values of the header and check them  for Host header injection attacks
    for curr_host_header in host_header_names:
        
        # Get the host header values as a list:
        host_headers_values = request_headers.getlist(curr_host_header)
        
        # If there are more than one header values, it means that the header was set more than once (HHI attack):
        if len(host_headers_values) > 1:
            return (True, f"{curr_host_header}: {host_headers_values}")
        
        host_header_to_check = host_headers_values[0]
        
        # ???
        if not re.match(r'^[a-zA-Z0-9.\-:]+$', host_header_to_check):
            return (True, f"{curr_host_header}: {host_header_to_check}")
        
        # If the header value contains any of the following characters, it means that the header was set more than once (HHI attack):
        if any(keyword in host_header_to_check.lower() for keyword in ['\r', '\n', '%0d', '%0a']):
            return (True, f"{curr_host_header}: {host_header_to_check}")
        
    return (False, None)
