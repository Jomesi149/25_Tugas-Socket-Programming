import socket
import threading
import queue

SERVER_IP = input("Masukkan IP untuk Server: ")  # Input IP dari admin server
SERVER_PORT = int(input("Masukkan Port untuk Server: "))  # Input port dari admin server
PASSWORD = input("Masukkan Password untuk Server: ")

clients = []
messages = queue.Queue()
usernames = set()

try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    print(f"Server running on {SERVER_IP}:{SERVER_PORT}")
except socket.error as e:
    if e.errno == 98:  # Port already in use
        print(f"Port {SERVER_PORT} sudah digunakan")
        SERVER_PORT = int(input("Masukkan Port lain: "))
        server_socket.bind((SERVER_IP, SERVER_PORT))
    else:
        print(f"Error: {e}")
        exit(1)

def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            if addr not in clients:
                clients.append(addr)
            for client in clients:
                try:
                    if message.decode().startswith("SIGNUP_TAG:"):
                        name = message.decode()[message.decode().index(":")+1:]
                        server_socket.sendto(f"{name} bergabung ke chatroom.".encode(), client)
                    else:
                        server_socket.sendto(message, client)
                except:
                    clients.remove(client)

def handle_client():
    while True:
        try:
            data, address = server_socket.recvfrom(1024)
            message = data.decode()

            if address not in clients:
                if message.startswith("PASSWORD "):
                    if message.split()[1] == PASSWORD:
                        server_socket.sendto(b"PASSWORD OK", address)
                    else:
                        server_socket.sendto(b"PASSWORD INCORRECT", address)
                elif message.startswith("USERNAME "):
                    username = message.split()[1]
                    if username in usernames:
                        server_socket.sendto(b"USERNAME TAKEN", address)
                    else:
                        usernames.add(username)
                        messages.put((f"SIGNUP_TAG:{username}".encode(), address))
                        server_socket.sendto(b"USERNAME OK", address)
                        print(f"{username} bergabung dari {address}")
            else:
                username = message.split(':')[0]
                print(f"{message}")
                messages.put((message.encode(), address))
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    print(f"Password: {PASSWORD}")
    
    broadcast_thread = threading.Thread(target=broadcast)
    broadcast_thread.daemon = True
    broadcast_thread.start()

    handle_thread = threading.Thread(target=handle_client)
    handle_thread.daemon = True
    handle_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nServer shutting down...")
        server_socket.close()