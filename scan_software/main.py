import flask

# Attack defense modules:
import xss

import waf_database
app = flask.Flask(__name__)  # Define the Flask app's name.
# waf = waf_database.MongoDB("127.0.0.1", 27017)
# waf.add_to_blacklist("11111", "XSS", "3", "True")
# waf.add_to_incoming_requests("11111", 3333, "XSS", True, "XSS", "11111")

def main():
    # Start the Flask app:
    app.run(host="0.0.0.0", port=3333)


# Function to handle each incoming request (it check for vulnerabilities in it):
@app.route("/<path:url>", methods=["GET", "HEAD", "DELETE", "POST", "PUT", "PATCH"])
@app.route("/", methods=["GET", "HEAD", "DELETE", "POST", "PUT", "PATCH"])
def handle_request(url=""):
    text_to_check = ""

    # Check the request's methods and act accordingly (because the request data (that we want to scan) is in different places):
    if flask.request.method in [ "GET", "HEAD", "DELETE" ]:
        text_to_check = flask.request.args
        
    elif flask.request.method in [ "POST", "PUT", "PATCH" ]:
        text_to_check = flask.request.form
    
    else:
        return "BLOCK{attack_name='Unknown Attack', blocked_text='Unknown Attack', count=0}"
    
    return check_for_vulnerabilities(text_to_check)


def check_for_vulnerabilities(request_data):
    """Function to check for vulnerabilities in the request data. If found, it return a BLOCK response.

    Args:
        request_data (werkzeug.datastructures.ImmutableMultiDict): The request data to check for vulnerabilities (the actual data is in HTTP request).

    Returns:
        str: ALLOW - No vulnerabilities found, BLOCK - Vulnerabilities found.
    """
    (is_xss, xss_text) = xss.is_request_xss(request_data)
    
    if is_xss:
        xss_text = xss_text.replace('"', '\\"')
        return f'BLOCK{{"attack_name":"XSS Attack", "blocked_text":"{xss_text}", "count":3}}'
    else:
        return "ALLOW"


if __name__ == "__main__":
    main()
    