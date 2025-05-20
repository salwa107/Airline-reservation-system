import socket

# Create a simple list to store bookings
bookings = []

HOST = 'localhost'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Server running on {HOST}:{PORT}...")

while True:
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")
    data = conn.recv(1024).decode()

    response = ""

    if data.startswith("BOOK "):
        name = data[5:]
        if name not in bookings:
            bookings.append(name)
            response = f"Seat booked for {name}"
        else:
            response = f"{name} already booked."

    elif data.startswith("CANCEL "):
        name = data[7:]
        if name in bookings:
            bookings.remove(name)
            response = f"Booking canceled for {name}"
        else:
            response = f"No booking found for {name}"

    elif data.startswith("SEARCH "):
        name = data[7:]
        if name in bookings:
            response = f"{name} has a booking."
        else:
            response = f"{name} does not have a booking."

    else:
        response = "Invalid command."

    conn.sendall(response.encode())
    conn.close()
