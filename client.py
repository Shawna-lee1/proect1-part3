import socket

# Define the server's host and port
server_host = 'localhost'  # Change to the actual server IP if needed
server_port = 12345

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((server_host, server_port))

# Receive the welcome message from the server
welcome_message = client_socket.recv(1024)
print(welcome_message.decode())

# Send a message to the server
message = "Hello, server!"
client_socket.send(message.encode())

# Receive a response from the server
response = client_socket.recv(1024)
print(f"Server response: {response.decode()}")

# Close the client socket
client_socket.close()
