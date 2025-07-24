import socket
import threading
import os
from datetime import datetime

# Server configuration
SERVER_HOST = "10.0.0.101"
SERVER_PORT = 12345
MAX_CLIENTS = 3
FILE_REPOSITORY = "server_files"  # Folder containing files to be shared

# Store client information
clients_cache = {}
clients_lock = threading.Lock()
active_clients = 0

# Ensure file repository exists
if not os.path.exists(FILE_REPOSITORY):
    os.makedirs(FILE_REPOSITORY)

def handle_client(client_socket, client_address, client_name):
    global active_clients
    with clients_lock:
        clients_cache[client_name] = {
            'address': client_address,
            'connected_at': datetime.now(),
            'disconnected_at': None
        }
    print(f"{client_name} connected from {client_address}")
    
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break  # Client disconnected
            
            if message.lower() == "exit":
                print(f"{client_name} disconnected.")
                break
            elif message.lower() == "status":
                status = "\n".join([f"{k}: {v['address']} - Connected at {v['connected_at']}" for k, v in clients_cache.items()])
                client_socket.send(status.encode())
            elif message.lower() == "list":
                files = os.listdir(FILE_REPOSITORY)
                file_list = "\n".join(files) if files else "No files available."
                client_socket.send(file_list.encode())
            elif message.startswith("get "):
                filename = message.split(" ", 1)[1]
                file_path = os.path.join(FILE_REPOSITORY, filename)
                if os.path.exists(file_path):
                    with open(file_path, "rb") as file:
                        client_socket.sendall(file.read())
                else:
                    client_socket.send("File not found".encode())
            else:
                response = f"{message} ACK"
                client_socket.send(response.encode())
    except Exception as e:
        print(f"Error with {client_name}: {e}")
    
    with clients_lock:
        clients_cache[client_name]['disconnected_at'] = datetime.now()
        active_clients -= 1
    client_socket.close()

def start_server():
    global active_clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(MAX_CLIENTS)
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")
    
    client_counter = 1
    
    while True:
        client_socket, client_address = server_socket.accept()
        
        with clients_lock:
            if active_clients >= MAX_CLIENTS:
                client_socket.send("Server full. Try again later.".encode())
                client_socket.close()
                continue
            active_clients += 1
            client_name = f"Client{client_counter:02d}"
            client_counter += 1
        
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address, client_name))
        thread.start()

if __name__ == "__main__":
    start_server()
