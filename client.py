import socket

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a specific address and port
s.bind(("localhost", 3333))

# listen for incoming connections
s.listen(1)

print("Listening on port 3333...")

# accept an incoming connection
conn, addr = s.accept()

print("Connection from", addr)

while True:
    # receive data from the connection
    data = conn.recv(1024)

    print("Received:", data.decode())

    conn.sendall(b"hello world")

# close the connection
conn.close()


# from flask import *
# app = Flask(__name__)

# @app.route("/<path:url>", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD", "TRACE", "CONNECT"])
# def index():
#     return "Hello World"

# if __name__ == "__main__":
#   app.run(host="0.0.0.0", port=3333, debug=False)