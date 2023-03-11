import flask
from datetime import datetime
import urllib.parse

# Attack defense modules:
import cross_site_scripting.xss
import sql_injection.sqli
import hpp
import http_host_header_injection
import open_redirect
import ssi_injection
import cross_site_tracing

# Import other custom modules:
import waf_database

# Define the Flask app and the database:
app = flask.Flask(__name__)
db = waf_database.MongoDB("127.0.0.1", 27017)  # Alon's IP: 172.17.0.2
    
    
def main():
    # Start the Flask app:
    app.run(host="0.0.0.0", port=3333)


# Function to handle each incoming request (it check for vulnerabilities in it):
@app.route("/<path:url>", methods=["GET", "HEAD", "DELETE", "POST", "PUT", "PATCH"])
@app.route("/", methods=["GET", "HEAD", "DELETE", "POST", "PUT", "PATCH"])
def handle_request(url=""):

    text_to_check = ""

    # Define the real client's IP and the raw request (for saving to the DB):
    client_ip = flask.request.headers.get("X-Forwarded-For", "0.0.0.0")
    raw_request = request_to_raw(flask.request)
    
    # If the client's IP is blocked, return BLACKLIST{...} string:
    if db.is_blocked(client_ip):
        attacks_performed = db.get_attacks_performed(client_ip)
        return f'BLACKLIST{{"attacks_performed":"{attacks_performed}"}}'
    
    # Check the request's methods and act accordingly (because the request data (that we want to scan) is in different places):
    if flask.request.method in [ "GET", "HEAD", "DELETE" ]:
        text_to_check = flask.request.args
        
    elif flask.request.method in [ "POST", "PUT", "PATCH" ]:
        text_to_check = flask.request.form
    
    elif flask.request.method == "TRACE":
        text_to_check = ""
        
    else:
        return f'BLOCK{{"attack_name": "Unsupported Request Method", "blocked_text": "HTTP Request", "count": 0}}'
    
    # Check if the request is dangerous and save the results to a tuple of (<name_of_detected_attack>, <where_the_attack_was_found>) [If safe: ("Safe", None)]:
    (attack_detected, blocked_text) = check_for_vulnerabilities(text_to_check, flask.request)
    
    # If no attack detected, add the request to the DB and return "ALLOW":
    if (attack_detected == "Safe"):
        db.add_to_incoming_requests(client_ip, raw_request, True, "", datetime.now())
        return "ALLOW"

    # If attack detected, add the request to the DB as a dangerous request.
    #  Then, add/edit the Blacklist and return BLOCK{...} or BLACKLIST{...} (if the client performed 3 attacks).
    else:
        db.add_to_incoming_requests(client_ip, raw_request, False, attack_detected, datetime.now())
        
        # If the client is in the Blacklist, edit his entry to be one more attack then before (unless he reached 3 attacks):
        if db.is_in_blacklist(client_ip):
            num_of_attacks = db.find_in_blacklist(client_ip)["Num of Attacks"] + 1
            db.update_blacklist(client_ip, num_of_attacks, attack_detected)
            
            if (num_of_attacks == waf_database.MAX_NUM_OF_ATTACKS):
                attacks_performed = db.get_attacks_performed(client_ip)
                return f'BLACKLIST{{"attacks_performed":"{attacks_performed}"}}'
                
            return f'BLOCK{{"attack_name": "{attack_detected}", "blocked_text": "{blocked_text}", "count" : {waf_database.MAX_NUM_OF_ATTACKS - num_of_attacks}}}'
        
        # If the client isn't in the Blacklist, add him and give him a counter of 1 attack:
        else:
            db.add_to_blacklist(client_ip, attack_detected, 1, False)
            return f'BLOCK{{"attack_name": "{attack_detected}", "blocked_text": "{blocked_text}", "count" : 2}}'


def check_for_vulnerabilities(request_data, full_request):
    """Function to check for vulnerabilities in the request data. If found, it return a BLOCK response.

    Args:
        request_data (werkzeug.datastructures.ImmutableMultiDict): The request data to check for vulnerabilities (the actual data is in HTTP request).

    Returns:
        str: ALLOW - No vulnerabilities found, BLOCK - Vulnerabilities found.
    """
    (is_xss, xss_text) = cross_site_scripting.xss.is_request_xss(request_data)
    (is_sqli, sqli_text) = sql_injection.sqli.is_request_sqli(request_data)
    (is_hhi, hhi_text) = http_host_header_injection.is_request_http_host_header(full_request.headers)
    (is_open_redirect, open_redirect_text) = open_redirect.is_request_open_redirect(full_request.url)
    (is_hpp, hpp_text) = hpp.is_request_hpp(request_data, full_request.url)
    (is_ssii, ssii_text) = ssi_injection.is_request_ssi_injection(request_data)
    (is_xst, xst_text) = cross_site_tracing.is_request_xst(full_request)
    
    if is_xss:
        xss_text = xss_text.replace('"', '\\"')
        return ("Cross-Site Scripting (XSS) / HTML Injection Attack", xss_text)
    if is_sqli:
        sqli_text = sqli_text.replace('"', '\\"')
        return ("SQL Injection Attack", sqli_text)
    elif is_hpp:
        hpp_text = hpp_text.replace('"', '\\"')
        return ("HTTP Parameter Pollution Attack", hpp_text)
    elif is_hhi:
        return ("Host Header Injection Attack", hhi_text)
    elif is_open_redirect:
        return ("Open Redirect Attack", open_redirect_text)
    elif is_ssii:
        ssii_text = ssii_text.replace('"', '\\"')
        return ("SSI Injection Attack", ssii_text)  
    elif is_xst:
        xst_text = xst_text.replace('"', '\\"')
        return ("Cross-Site Tracing (XST) Attack", xst_text)
    else:
        return ("Safe", None)


def request_to_raw(flask_request):
    """Function to convert the Flask request to a raw HTTP request (for saving to the DB).
    For example (returned string):
        GET / HTTP/1.1
        Host: www.example.com
    
    Args:
        flask_request (flask.request): The Flask request to convert.

    Returns:
        str: The raw HTTP request.
    """
    request_lines = [ f"{flask_request.method} {flask_request.path} {flask_request.environ['SERVER_PROTOCOL']}" ]
    
    for key, value in flask_request.headers:
        request_lines.append(f"{key}: {value}")
    
    if flask_request.form:
        request_lines.append(" ")
        request_lines.append(urllib.parse.urlencode(flask_request.form, doseq=False))

    return "\n".join(request_lines)


if __name__ == "__main__":
    main()
    
