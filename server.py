import os
import sys
import socket
import multiprocessing
import signal

# Function to handle each client connection
def handle_connection(client_socket, connection_id, file_dir):
    # Create a file path for the current connection
    file_path = os.path.join(file_dir, f"{connection_id}.file")
    
    try:
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

# Function to gracefully handle signals
def signal_handler(signum, frame):
    print("Received signal, exiting gracefully...")
    sys.exit(0)

# Main function
def main():
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
        # Use multiprocessing to handle multiple connections simultaneously
        processes = []
        while True:
            # Accept a new connection
            client_socket, addr = server_socket.accept()
            
            # Create a new process to handle the connection
            connection_id = len(processes) + 1
            p = multiprocessing.Process(target=handle_connection, args=(client_socket, connection_id, file_dir))
            p.start()
            processes.append(p)
    
    except KeyboardInterrupt:
        print("Server terminated by user.")
    
    finally:
        # Close the server socket and wait for all processes to finish
        server_socket.close()
        for p in processes:
            p.join()

if __name__ == "__main__":
    main()





