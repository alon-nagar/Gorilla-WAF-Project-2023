import re

def is_request_http_host_header(request_headers):
    """
        Function to check if a request contains a Host Header injection attack.
        A Host Header Injection (HHI) attack occurs when an attacker modifies the value of the Host header to include malicious
        code or characters, such as line breaks or null characters, which can allow the attacker to bypass security controls.
        
        Args:
            request_headers (werkzeug.datastructures.Headers): The HTTP request's headers.
            
        Returns:
            tuple: (True, "{header_name}: {header_val}"): A tuple of (True - HHI detected, str - The header name and value where HHI was detected).
    """
    
    # Define the headers to check for HHI attacks (there are several headers that can be used to set the Host header):
    host_header_names = ['Host', 'X-Forwarded-Host', 'X-Host', 'X-Forwarded-Server', 'X-HTTP-Host-Override', 'Forwarded']
    
    # For each header name, get all the values of the header and check them for HHI attacks
    for curr_host_header in host_header_names:
        
        # Get the host header values as a list:
        host_headers_values = request_headers.getlist(curr_host_header)
        
        # If there are more than one header value, it means that the header was set more than once (HHI attack):
        if len(host_headers_values) > 1:
            return (True, f"{curr_host_header}: {host_headers_values}")
        
        # If there is no header value, move to the next header name:
        if len(host_headers_values) == 0:
            continue
        
        # Get the header value to check for HHI attacks:
        host_header_to_check = host_headers_values[0]
        
        # Check if the header value contains any illegal characters or patterns that might indicate an HHI attack:
        if not re.match(r'^[a-zA-Z0-9.\-:%]+\Z', host_header_to_check):
            return (True, f"{curr_host_header}: {host_header_to_check}")
        
    # If no HHI attack was detected in any of the headers, return False:
    return (False, None)