from flask import jsonify, request, Flask
import gui_database
import scan_software_files
import linux_commands

DB_FLASK_PORT = 4444
ALLOWED_REDIRECT_URLS_FILE_PATH = "../Gorilla-ScanSoftware/attacks/open_redirect/allowed_redirection_urls.txt"

# Define the Flask app and other variables:
app = Flask(__name__)
db = gui_database.MongoDB("172.17.0.2", 27017)  # Alon's IP: 172.17.0.2
allowed_urls = scan_software_files.AllowedRedirectURLs(ALLOWED_REDIRECT_URLS_FILE_PATH)
linux_cmd = linux_commands.LinuxCMD()


def main():
    app.run(host="0.0.0.0", port=DB_FLASK_PORT)


# Add CORS headers to all responses
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# In the following functions, we handle requests to get data from the database.

# ------------------------------------[ INCOMING REQUESTS ]------------------------------------
@app.route("/get_all_incoming_requests", methods=["GET"])
def handle_get_all_incoming_requests():
    return db.get_all_incoming_requests()

@app.route("/get_request_by_id", methods=["GET"])
def handle_get_request_by_id():
    try:
        id = request.args.getlist("id")[0]
        id.strip()
        if id != "":
            return db.get_request_by_id(id)
        return "ID can't be empty"
    
    except:
        return "No ID was given"


# ----------------------------------------[ BLACKLIST ]----------------------------------------
@app.route("/get_all_blacklist", methods=["GET"])
def handle_get_all_blacklist():
    return db.get_all_blacklist()

@app.route("/get_blacklist_entry_by_ip", methods=["GET"])
def handle_get_blacklist_entry_by_ip():
    try:
        ip_address = request.args.getlist("ip_address")[0]
        ip_address.strip()
        if ip_address != "":
            return db.get_blacklist_entry_by_ip(ip_address)
        return "IP can't be empty"
    
    except:
        return "No IP address was given"
    
@app.route("/add_ip_to_blacklist", methods=["GET"])
def handle_add_ip_to_blacklist():
    try:
        ip_address = request.args.getlist("ip_address")[0]
        ip_address.strip()
        if ip_address != "":
            return db.add_ip_to_blacklist(ip_address)
        return "IP can't be empty"
    
    except:
        return "No IP address was given"

@app.route("/remove_ip_from_blacklist", methods=["GET"])
def handle_remove_ip_from_blacklist():
    try:
        ip_address = request.args.getlist("ip_address")[0]
        ip_address.strip()
        if ip_address != "":
            return db.remove_ip_from_blacklist(ip_address)
        return "IP can't be empty"
    
    except:
        return "No IP address was given"


# ----------------------------------------[ ALLOWED REDIRECT URLS ]----------------------------------------
@app.route("/get_all_allowed_redirect_urls", methods=["GET"])
def handle_get_all_allowed_redirect_urls():
    return jsonify(allowed_urls.get_allowed_urls())

@app.route("/add_url_to_allowed_redirect_urls", methods=["GET"])
def handle_add_url_to_allowed_redirect_urls():
    try:
        url = request.args.getlist("url")[0]
        url.strip()
        if url != "":
            return allowed_urls.add_url(url)
        return "URL can't be empty"
    
    except:
        return "No URL was given"

@app.route("/remove_url_from_allowed_redirect_urls", methods=["GET"])
def handle_remove_url_from_allowed_redirect_urls():
    try:
        url = request.args.getlist("url")[0]
        url.strip()
        if url != "":
            return allowed_urls.remove_url(url)
        return "URL can't be empty"
    
    except:
        return "No URL was given"
    

# ----------------------------------------[ WAF START/STOP ]----------------------------------------
@app.route("/start_waf", methods=["GET"])
def handle_start_waf():
    return linux_cmd.start_waf()


@app.route("/stop_waf", methods=["GET"])
def handle_stop_waf():
    return linux_cmd.stop_waf()


@app.route("/get_waf_status", methods=["GET"])
def handle_get_waf_status():
    return linux_cmd.get_waf_status()


if __name__ == "__main__":
    main()
    