import socket
import threading
import sys

SERVER_IP = input("Masukkan IP Server: ")
SERVER_PORT = int(input("Masukkan Port Server: "))  # Input port dari user

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def clear_screen():
    #Untuk membersihkan tampilan terminal
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()

def clear_last_line():
    #untuk menghapus baris terakhir setelah input message
    sys.stdout.write("\033[F\033[K")
    sys.stdout.flush()

def receive_messages():
    #untuk menerima hasil broadcast dari server
    while True:
        try:
            message, _ = client_socket.recvfrom(1024)
            print(message.decode() + "\n> ", end="")
        except:
            break

def join_chatroom():
    while True:  # Loop untuk password
        password = input("Masukkan password: ")
        client_socket.sendto(f"PASSWORD {password}".encode(), (SERVER_IP, SERVER_PORT))
        try:
            response, _ = client_socket.recvfrom(1024)
        except socket.timeout:
            print("Timeout: Server tidak merespon. Periksa IP dan Port.")
            return None

        if response.decode() == "PASSWORD OK":
            break
        else:
            print("Password salah! Coba lagi.")
    
    while True: # Loop untuk username
        username = input("Masukkan username: ")
        client_socket.sendto(f"USERNAME {username}".encode(), (SERVER_IP, SERVER_PORT))
        response, _ = client_socket.recvfrom(1024)
        if response.decode() == "USERNAME OK":
            clear_screen()
            print("Bergabung dengan chatroom...")
            return username
        elif response.decode() == "USERNAME TAKEN":
            print("Username telah digunakan!")
        else:
            print("Terjadi kesalahan. Coba lagi.")

def main():
    # Tambahkan timeout untuk menangani koneksi yang gagal
    client_socket.settimeout(5)
    try:
        username = join_chatroom()
        if username:
            # Reset timeout setelah berhasil terhubung
            client_socket.settimeout(None)
            
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
                    
                formatted_message = f"{username}: {message}"
                client_socket.sendto(formatted_message.encode(), (SERVER_IP, SERVER_PORT))

    except ValueError:
        print("Port harus berupa angka!")
    except ConnectionRefusedError:
        print("Koneksi ditolak. Periksa IP dan Port.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()