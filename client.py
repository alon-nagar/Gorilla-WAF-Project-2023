# #print("a")





# import socket

# HOST = 'localhost'  # The server's hostname or IP address
# PORT = 3333        # The port used by the server

# # Create a socket object
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Bind the socket to the host and port
# s.bind((HOST, PORT))

# # Listen for incoming connections
# s.listen()
# print("Listening for incoming connections...")

# while True:
#     # Wait for a client to connect
#     conn, addr = s.accept()
#     print(f"Connection from {addr} has been established.")

#     # Receive the data sent by the client
#     data = conn.recv(1024)
#     print(f"Data received: {data.decode()}")

#     # Send a response to the client
#     conn.sendall("Data received".encode())

#     # Close the connection
#     conn.close()








# import socket

# # create a socket object
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # bind the socket to a specific address and port
# s.bind(("localhost", 3333))

# # listen for incoming connections
# s.listen(1)

# print("Listening on port 3333...")

# while True:
#     # accept an incoming connection
#     conn, addr = s.accept()

#     print("Connection from", addr)


#     # conn, addr = s.accept()

#     # receive data from the connection
#     data = conn.recv(1024)

#     print("Received:", data.decode())


#     # send the "hello world" response
#     #conn.sendall(b"hello world")

#     # close the connection
#     conn.close()








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

# receive data from the connection
data = conn.recv(1024)

print("Received:", data.decode())

conn.sendall(b"hello world")

# close the connection
conn.close()
