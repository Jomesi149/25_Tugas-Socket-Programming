import sys
def clear_screen():
    # Untuk membersihkan tampilan terminal
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()

def clear_last_line():
    # Untuk menghapus baris terakhir setelah input message
    sys.stdout.write("\033[F\033[K")
    sys.stdout.flush()
