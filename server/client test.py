import socket

def main():
    host = 'localhost'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        welcome = client_socket.recv(1024).decode()
        print(welcome)

        while True:
            command = input("Enter command (BOOK <name> <seat> / LIST / QUIT): ")
            client_socket.sendall(command.encode())

            response = client_socket.recv(4096).decode()
            print("Server response:\n" + response)

            if command.strip().upper() == 'QUIT':
                break

if __name__ == '__main__':
    main()
