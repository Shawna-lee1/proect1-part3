import socket

host = '0.0.0.0'  # Listen on all available network interfaces
port = 12345     

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(5)  # Listen for up to 5 connections

print(f"Server is listening on {host}:{port}")

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")
    
    # Send a welcome message to the client
    message = "Welcome to the server!"
    client_socket.send(message.encode())
    
    # Receive data from the client
    data = client_socket.recv(1024)
    if not data:
        break
    
    print(f"Received data from client: {data.decode()}")
    
    # Send a response back to the client
    response = "Server received your message."
    client_socket.send(response.encode())
    
    # Close the client socket
    client_socket.close()

# Close the server socket when done
server_socket.close()
