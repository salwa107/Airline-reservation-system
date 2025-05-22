import socket
from OurPROJECT import book_seat, list_reservations

HOST = '0.0.0.0'  # to accept external connections
PORT = 12345

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    conn.sendall(b"Welcome to the Airline Booking Server!\n")

    while True:
        data = conn.recv(1024).decode().strip()
        if not data:
            break

        print(f"Received from {addr}: {data}")

        if data.upper() == "QUIT":
            conn.sendall(b"Goodbye!\n")
            break

        elif data.upper() == "LIST":
            reservations = list_reservations()
            if reservations:
                response = "\n".join([f"{r['name']} -> Seat {r['seat']}" for r in reservations])
            else:
                response = "No reservations found."
            conn.sendall(response.encode() + b"\n")

        elif data.upper().startswith("BOOK"):
            try:
                _, name, seat = data.split()
                result = book_seat(name, seat)
                conn.sendall(result.encode() + b"\n")
            except ValueError:
                conn.sendall(b"Invalid BOOK format. Use: BOOK <name> <seat>\n")
        else:
            conn.sendall(b"Unknown command.\n")

    conn.close()
    print(f"Connection closed: {addr}")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server running on {HOST}:{PORT} (accessible from network)...")

        while True:
            conn, addr = server_socket.accept()
            handle_client(conn, addr)

if __name__ == "__main__":
    start_server()
