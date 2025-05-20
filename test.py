import socket        #test this on your pc from your terminal

HOST = 'localhost'
PORT = 12345

def send_request(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(command.encode())
        response = s.recv(1024).decode()
        print("Server:", response)

# Example usage
send_request("BOOK Hamza")
send_request("SEARCH Hamza")
send_request("CANCEL Hamza")
send_request("SEARCH Hamza")
