import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import socket
import threading
import queue

# === Server Class ===
class ChatServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.running = False

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        while self.running:
            try:
                client_socket, _ = self.server_socket.accept()
                self.clients.append(client_socket)
                threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()
            except Exception as e:
                print("Error accepting connection:", e)

    def handle_client(self, client_socket):
        while self.running:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                self.broadcast(message, client_socket)
            except:
                break
        client_socket.close()
        if client_socket in self.clients:
            self.clients.remove(client_socket)

    def broadcast(self, message, sender_socket):
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    pass

    def stop(self):
        self.running = False
        for client in self.clients:
            client.close()
        if self.server_socket:
            self.server_socket.close()

# === Chat GUI ===
class ChatApp:
    def __init__(self, root, is_server=False):
        self.root = root
        self.is_server = is_server
        self.message_queue = queue.Queue()
        self.root.title("Server Chat" if is_server else "Client Chat")

        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
        self.chat_area.pack(padx=10, pady=10)
        self.chat_area.config(state=tk.DISABLED)

        self.message_entry = tk.Entry(root, width=40)
        self.message_entry.pack(padx=10, pady=5, side=tk.LEFT)

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=5, side=tk.LEFT)

        if is_server:
            self.server = ChatServer()
            self.server.start()
            self.display_message("Server started.")
            self.send_func = self.broadcast_message
        else:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.client_socket.connect(('localhost', 12345))
                threading.Thread(target=self.receive_messages, daemon=True).start()
                self.send_func = self.send_message_to_server
            except:
                self.display_message("❌ Could not connect to server.")
                self.disable_input()

        self.root.after(100, self.check_messages)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def send_message(self):
        msg = self.message_entry.get().strip()
        if msg:
            self.send_func(msg)
            self.message_entry.delete(0, tk.END)

    def send_message_to_server(self, msg):
        try:
            self.client_socket.send(msg.encode('utf-8'))
            self.display_message("You: " + msg)
        except:
            self.display_message("Failed to send message.")

    def broadcast_message(self, msg):
        self.display_message("Admin: " + msg)
        self.server.broadcast("Admin: " + msg, None)

    def receive_messages(self):
        while True:
            try:
                msg = self.client_socket.recv(1024).decode('utf-8')
                if not msg:
                    break
                self.message_queue.put(msg)
            except:
                break

    def display_message(self, msg):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, msg + "\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    def disable_input(self):
        self.message_entry.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)

    def check_messages(self):
        while not self.message_queue.empty():
            self.display_message(self.message_queue.get())
        self.root.after(100, self.check_messages)

    def on_close(self):
        if self.is_server:
            self.server.stop()
        else:
            try:
                self.client_socket.close()
            except:
                pass
        self.root.destroy()

# === Launcher Window ===
def launch_selector():
    root = tk.Tk()
    root.withdraw()
    choice = simpledialog.askstring("Start Chat", "Type 'server' or 'client':")
    if choice and choice.lower() == "server":
        main_window = tk.Tk()
        ChatApp(main_window, is_server=True)
        main_window.mainloop()
    elif choice and choice.lower() == "client":
        main_window = tk.Tk()
        ChatApp(main_window, is_server=False)
        main_window.mainloop()
    else:
        messagebox.showinfo("Cancelled", "No valid selection made.")

if __name__ == "__main__":
    launch_selector()
