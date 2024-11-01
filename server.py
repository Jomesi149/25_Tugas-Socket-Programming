import socket
import threading
import queue

SERVER_IP = input("Masukkan IP untuk Server: ")  # Input IP dari admin server
SERVER_PORT = int(input("Masukkan Port untuk Server: "))  # Input port dari admin server
PASSWORD = input("Masukkan Password untuk Server: ") # Input password dari admin server

clients = []
messages = queue.Queue()
usernames = {}

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
            for client in clients:
                try:
                    server_socket.sendto(message, client)
                except socket.error as e:
                    # Handle disconnection errors gracefully
                    if client in clients:
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
                    if username in usernames.values():
                        server_socket.sendto(b"USERNAME TAKEN", address)
                    else:
                        usernames[address] = username
                        clients.append(address)
                        messages.put((f"{username} bergabung ke chatroom.".encode(), address))
                        server_socket.sendto(b"USERNAME OK", address)
                        print(f"{username} bergabung dari {address}")
            else:
                if message.lower().strip() == "exit":
                    username = usernames.pop(address, "User")
                    exit_message = f"{username} telah keluar dari chatroom."
                    messages.put((exit_message.encode(), address))
                    clients.remove(address)
                    print(exit_message)
                else:
                    print(f"{message}")
                    messages.put((message.encode(), address))
        except socket.error as e:
            if e.errno == 10054:
                continue
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
        print("\\nServer shutting down...")
        server_socket.close()
