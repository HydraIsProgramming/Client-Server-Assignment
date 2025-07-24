import socket

# Client configuration
SERVER_HOST = "10.0.0.101"
SERVER_PORT = 12345

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("Connected to server. Type messages, 'status' for server status, 'list' for files, 'get <filename>' to download, 'exit' to disconnect.")
    except Exception as e:
        print(f"Could not connect: {e}")
        return
    
    while True:
        message = input("You: ")
        client_socket.send(message.encode())
        
        if message.lower() == "exit":
            break
        
        response = client_socket.recv(1024).decode()
        print(f"Server: {response}")
    
    client_socket.close()
    print("Disconnected from server.")

if __name__ == "__main__":
    start_client()
