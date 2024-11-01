import socket
import threading
import sys

SERVER_IP = input("Masukkan IP Server: ")
SERVER_PORT = int(input("Masukkan Port Server: "))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def clear_screen():
    # Untuk membersihkan tampilan terminal
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()

def clear_last_line():
    # Untuk menghapus baris terakhir setelah input message
    sys.stdout.write("\033[F\033[K")
    sys.stdout.flush()


def receive_messages():
    while True:
        try:
            message, _ = client_socket.recvfrom(1024)
            print(message.decode() + "\n> ", end="")
        except:
            print("Terputus dari server.")
            break

# Loop untuk verifikasi password
while True:
    password = input("Masukkan Password: ")
    client_socket.sendto(f"PASSWORD {password}".encode(), (SERVER_IP, SERVER_PORT))
    password_response, _ = client_socket.recvfrom(1024)

    if password_response.decode() == "PASSWORD OK":
        break
    else:
        print("Password salah, coba lagi.")

# Loop untuk verifikasi username
while True:
    username = input("Masukkan Username: ")
    client_socket.sendto(f"USERNAME {username}".encode(), (SERVER_IP, SERVER_PORT))
    username_response, _ = client_socket.recvfrom(1024)

    if username_response.decode() == "USERNAME OK":
        break
    elif username_response.decode() == "USERNAME TAKEN":
        print("Username sudah digunakan. Coba username lain.")
    else:
        print("Terjadi kesalahan, coba lagi.")

# Setelah berhasil login, bersihkan layar dan tampilkan pesan selamat datang
clear_screen()
print(f"Anda bergabung sebagai {username}")

# Mulai thread untuk menerima pesan dari server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

# Loop untuk mengirim pesan
while True:
    message = input("> ")
    clear_last_line()
    if message.lower() == "exit":
        client_socket.sendto("exit".encode(), (SERVER_IP, SERVER_PORT))
        print("Anda telah keluar dari chatroom.")
        break
    client_socket.sendto(f"{username}: {message}".encode(), (SERVER_IP, SERVER_PORT))

client_socket.close()
