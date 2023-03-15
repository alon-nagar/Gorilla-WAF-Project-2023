import flask
import gui_database


# Define the Flask app and the database:
app = flask.Flask(__name__)
db = gui_database.MongoDB("172.17.0.2", 27017)  # Alon's IP: 172.17.0.2
  

def main():
    # Start the Flask app:
    app.run(host="0.0.0.0", port=4444)


@app.route("/get_incoming_requests", methods=["GET"])
def handle_get_incoming_requests():
    return db.get_incoming_requests_collection()


@app.route("/get_blacklist", methods=["GET"])
def handle_get_blacklist():
    return db.get_blacklist_collection()


@app.route("/add_ip_to_blacklist", methods=["POST"])
def handle_add_ip_to_blacklist():
    ip_address = flask.request.args.getlist("ip_address")[0]
    return db.add_ip_to_blacklist(ip_address)


@app.route("/delete_ip_from_blacklist", methods=["POST"])
def handle_delete_ip_from_blacklist():
    ip_address = flask.request.args.getlist("ip_address")[0]
    return db.delete_ip_from_blacklist(ip_address)


if __name__ == "__main__":
    main()
    
