import socket
import threading
import queue

SERVER_IP = "0.0.0.0"
SERVER_PORT = 12345
PASSWORD = "securepassword"

clients = []
messages = queue.Queue()
usernames = set()  # Untuk menyimpan username yang sudah digunakan

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
print(f"Server running on {SERVER_IP}:{SERVER_PORT}")

def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            print(message.decode())
            if addr not in clients:
                clients.append(addr)
            for client in clients:
                try:
                    if message.decode().startswith("SIGNUP_TAG:"):
                        name = message.decode()[message.decode().index(":")+1:]
                        server_socket.sendto(f"{name} udah masuk, pelan pelan yah.".encode(), client)
                    else:
                        server_socket.sendto(message, client)
                except:
                    clients.remove(client)

def handle_client():
    while True:
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
                    print(f"{username} joined from {address}")
        else:
            username = message.split(':')[0]
            print(f"{username}@{address}: {message}")
            messages.put((message.encode(), address))

threading.Thread(target=handle_client).start()
threading.Thread(target=broadcast).start()