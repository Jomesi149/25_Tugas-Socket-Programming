import socket

SERVER_IP = input("Masukkan IP Server: ")
SERVER_PORT = 12345
PASSWORD = "securepassword"
USERNAME = input("Masukkan username unik Anda: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def join_chatroom():
    client_socket.sendto(f"PASSWORD {PASSWORD}".encode(), (SERVER_IP, SERVER_PORT))         # mengirim password
    response, _ = client_socket.recvfrom(1024)
    if response.decode() == "PASSWORD OK":

        client_socket.sendto(f"USERNAME {USERNAME}".encode(), (SERVER_IP, SERVER_PORT))     # mengirim username jika password benar
        response, _ = client_socket.recvfrom(1024)
        if response.decode() == "USERNAME OK":
            print("Bergabung dengan chatroom...")
            return True
        else:
            print("Username telah digunakan!")
            return False
    else:
        print("Password salah!")
        return False

if join_chatroom():
    print("Ketik 'exit' untuk keluar.")                                                     # jika ingin keluar dari chatroom
    while True:

        message = input("> ")
        if message.lower() == "exit":
            print("Keluar dari chatroom...")
            client_socket.close()
            break

        client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

        try:
            client_socket.settimeout(1.0)
            message, _ = client_socket.recvfrom(1024)
            print("\n" + message.decode() + "\n> ", end="")
        except socket.timeout:
            continue
else:
    client_socket.close()