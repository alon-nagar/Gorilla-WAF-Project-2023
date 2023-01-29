import flask

app = flask.Flask(__name__)  # Define the Flask app's name.

def main():
    # Start the Flask app:
    app.run(host="0.0.0.0", port=3333, debug=False)


# Function to handle each incoming request (it check for vulnerabilities in it):
@app.route("/<path:url>", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD", "TRACE", "CONNECT"])
@app.route("/", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD", "TRACE", "CONNECT"])
def handle_request(url=""):
    text_to_check = ""
    
    if flask.request.method == "GET":
        text_to_check = flask.request.args
    elif flask.request.method == "POST":
        text_to_check = flask.request.form
        
    return check_for_vulnerabilities(text_to_check)


def check_for_vulnerabilities():
    pass  # TODO: Implement this function.


if __name__ == "__main__":
    main()
    