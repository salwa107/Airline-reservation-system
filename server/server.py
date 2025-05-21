import socket
import threading
from ourproject import book_seat, list_reservations

HOST = 'localhost'
PORT = 12345

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.sendall(b"Welcome to the Airline Reservation Server!\n")

    while True:
        try:
            conn.sendall(b"\nCommands:\n1. BOOK <name> <seat>\n2. LIST\n3. QUIT\nEnter command: ")
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            print(f"[{addr}] Command received: {data}")
            parts = data.split()

            if parts[0].upper() == 'BOOK' and len(parts) == 3:
                name = parts[1]
                seat = parts[2]
                result = book_seat(name, seat)
                conn.sendall(result.encode() + b"\n")

            elif parts[0].upper() == 'LIST':
                res_list = list_reservations()
                if not res_list:
                    conn.sendall(b"No reservations yet.\n")
                else:
                    for res in res_list:
                        line = f"{res['name']} - Seat {res['seat']}\n"
                        conn.sendall(line.encode())

            elif parts[0].upper() == 'QUIT':
                conn.sendall(b"Goodbye!\n")
                break

            else:
                conn.sendall(b"Invalid command.\n")

        except ConnectionResetError:
            break

    conn.close()
    print(f"[DISCONNECTED] {addr} disconnected.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[STARTED] Server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
