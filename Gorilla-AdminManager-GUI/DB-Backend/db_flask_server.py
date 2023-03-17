from flask import jsonify, request, Flask
import gui_database

DB_FLASK_PORT = 4444

# Define the Flask app and the database:
app = Flask(__name__)
db = gui_database.MongoDB("172.17.0.2", 27017)  # Alon's IP: 172.17.0.2


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


if __name__ == "__main__":
    main()
    