import socket
import threading

SERVER_IP = "0.0.0.0"                                               # 0.0.0.0 artinya bisa dimasukin server bebas
SERVER_PORT = 12345                                                 # port default
PASSWORD = "securepassword"                                         # password utk client

clients = {}                                                        # utk simpan username & address client

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))                        # bind server
print(f"Server running on {SERVER_IP}:{SERVER_PORT}")               # menunjukkan server ip & port

def broadcast(message, sender_address):                             # menampilkan pesan yg dikirim client
    for client_address in clients:
        if client_address != sender_address:
            server_socket.sendto(message, client_address)

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
                if username in clients.values():
                    server_socket.sendto(b"USERNAME TAKEN", address)
                else:
                    clients[address] = username
                    server_socket.sendto(b"USERNAME OK", address)
                    print(f"{username} joined from {address}")
        else:
            username = clients[address]
            print(f"{username}@{address}: {message}")
            broadcast(f"{username}: {message}".encode(), address)

threading.Thread(target=handle_client).start()