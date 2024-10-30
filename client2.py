import socket
import threading
import sys

SERVER_IP = input("Masukkan IP Server: ")
SERVER_PORT = 12345
PASSWORD = "securepassword"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def clear_last_line():
    # Menggerakkan kursor ke atas dan menghapus baris
    sys.stdout.write("\033[F\033[K")
    sys.stdout.flush()

def receive_messages():
    while True:
        try:
            message, _ = client_socket.recvfrom(1024)
            print(message.decode() + "\n> ", end="")
        except:
            break

def join_chatroom():
    # Kirim password
    client_socket.sendto(f"PASSWORD {PASSWORD}".encode(), (SERVER_IP, SERVER_PORT))
    response, _ = client_socket.recvfrom(1024)
    
    if response.decode() == "PASSWORD OK":
        # Kirim username jika password benar
        while True:
            username = input("Masukkan username: ")
            client_socket.sendto(f"USERNAME {username}".encode(), (SERVER_IP, SERVER_PORT))
            response, _ = client_socket.recvfrom(1024)
            if response.decode() == "USERNAME OK":
                print("Bergabung dengan chatroom...")
                return username
            elif response.decode() == "USERNAME TAKEN":
                print("Username telah digunakan!")
            else:
                print("Terjadi kesalahan. Coba lagi.")
    else:
        print("Password salah!")
        return None

def main():
    username = join_chatroom()
    if username:
        # Mulai thread untuk menerima pesan
        receive_thread = threading.Thread(target=receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

        print("Ketik 'exit' untuk keluar.")
        
        while True:
            message = input("> ")
            clear_last_line()
            if message.lower() == 'exit':
                print("Keluar dari chatroom...")
                break
                
            # Format pesan dengan username
            formatted_message = f"{username}: {message}"
            client_socket.sendto(formatted_message.encode(), (SERVER_IP, SERVER_PORT))

    client_socket.close()

if __name__ == "__main__":
    main()