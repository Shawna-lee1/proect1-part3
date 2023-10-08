import socket
import sys

# Define the server's host and port
server_host = 'localhost'  # Change to the actual server IP if needed
server_port = 12345

# Define the file to send (change as needed)
file_to_send = "sample.txt"

def send_file_data(client_socket):
    try:
        with open(file_to_send, "rb") as file:
            while True:
                data = file.read(4096)
                if not data:
                    break
                client_socket.send(data)
    except Exception as e:
        print(f"Error sending file data: {e}")

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect((server_host, server_port))

    # Receive the welcome message from the server
    welcome_message = client_socket.recv(1024)
    print(welcome_message.decode())

    # Send the file data to the server
    send_file_data(client_socket)

    # Close the client socket
    client_socket.close()

except ConnectionRefusedError:
    print("ERROR: Server is not running or refused the connection.")
except FileNotFoundError:
    print(f"ERROR: File '{file_to_send}' not found.")
except KeyboardInterrupt:
    print("Client terminated by user.")
except Exception as e:
    print(f"Error: {e}")

