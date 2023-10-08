import os
import sys
import socket
import threading
import signal
import time

# Global variables to track connection count and file directory
connection_count = 0
file_dir = ""

# Lock to ensure synchronized access to connection_count
connection_lock = threading.Lock()

# Function to handle each client connection
def handle_connection(client_socket, connection_id):
    global file_dir
    
    # Create a file path for the current connection
    file_path = os.path.join(file_dir, f"{connection_id}.file")
    
    try:
        # Set a timeout for the connection
        client_socket.settimeout(10)
        
        # Send the "accio" command to the client
        client_socket.send(b"accio\r\n")
        
        # Open the file for writing in binary mode
        with open(file_path, "wb") as file:
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                
                # Write the received data to the file
                file.write(data)
                
        print(f"Connection {connection_id} received and saved.")
    
    except socket.timeout:
        # Handle timeout (no data received for 10 seconds)
        error_msg = "ERROR"
        with open(file_path, "wb") as file:
            file.write(error_msg.encode())
        print(f"Connection {connection_id} timed out and saved an error message.")
    
    except Exception as e:
        print(f"Error in connection {connection_id}: {e}")
    
    finally:
        # Close the client socket
        client_socket.close()

        # Release the lock to allow another thread to increment the count
        with connection_lock:
            connection_count -= 1

# Function to gracefully handle signals
def signal_handler(signal, frame):
    print("Received signal, exiting gracefully...")
    sys.exit(0)

# Main function
def main():
    global connection_count, file_dir
    
    # Check command-line arguments
    if len(sys.argv) != 3:
        sys.stderr.write("ERROR: Usage: python3 server.py <PORT> <FILE-DIR>\n")
        sys.exit(1)
    
    port = int(sys.argv[1])
    
    # Check if the port is within the valid range
    if not (0 <= port <= 65535):
        sys.stderr.write("ERROR: Port must be in the range 0-65535.\n")
        sys.exit(1)
    
    file_dir = sys.argv[2]
    
    # Validate the FILE-DIR path
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    
    # Register signal handlers for graceful exit
    signal.signal(signal.SIGQUIT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create a listening socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(10)  # Allow up to 10 pending connections
    
    print(f"Server is listening on port {port}")
    
    try:
        while True:
            # Accept a new connection
            client_socket, addr = server_socket.accept()
            
            # Increment the connection count
            with connection_lock:
                connection_count += 1
            
            # Start a new thread to handle the connection
            t = threading.Thread(target=handle_connection, args=(client_socket, connection_count))
            t.start()
    
    except KeyboardInterrupt:
        print("Server terminated by user.")
    
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()




