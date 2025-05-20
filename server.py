import socket
import threading
import pickle
from airline_system import AirlineSystem  # existing system code made into a class

HOST = 'localhost'
PORT = 12345

airline_system = AirlineSystem()

def handle_client(client_socket):
    try:
        data = client_socket.recv(4096)
        if not data:
            return
        request = pickle.loads(data)
        command = request.get("command")
        payload = request.get("payload")

        if command == "book":
            result = airline_system.book_seat(payload)
        elif command == "cancel":
            result = airline_system.cancel_booking(payload)
        elif command == "search":
            result = airline_system.search_flight(payload)
        else:
            result = "Unknown command."

        client_socket.send(pickle.dumps(result))
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server started on {HOST}:{PORT}")
    while True:
        client_socket, addr = server.accept()
        print(f"Connected by {addr}")
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
