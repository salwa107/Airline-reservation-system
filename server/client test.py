import socket
import json

def book_seat():
    name = input("Enter your name: ")
    seat = input("Enter seat number (e.g., 3A): ")

    request = {
        "command": "book",
        "name": name,
        "seat": seat
    }

    return request

def main():
    host = 'localhost'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        request = book_seat()

        client_socket.send(json.dumps(request).encode())
        response = client_socket.recv(4096).decode()
        print("Server response:", response)

if __name__ == '__main__':
    main()
