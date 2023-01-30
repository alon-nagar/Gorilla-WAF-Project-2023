import flask

# Attack defense:
import xss

app = flask.Flask(__name__)  # Define the Flask app's name.

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
    (is_xss, xss_text) = xss.is_xss(request_data)
    
    if is_xss:
        return f"BLOCK{{attack_name='XSS Attack', blocked_text={xss_text}, count=3}}"
    else:
        return "ALLOW"


if __name__ == "__main__":
    main()
    