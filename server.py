import socket
import threading

def handle_client(client_socket, clients, usernames):
    username = client_socket.recv(1024).decode("utf-8")
    usernames[client_socket] = username
    welcome_message = f"{username} has joined the chat."
    broadcast(welcome_message, client_socket, clients)

    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                broadcast(f"{username}: {message}", client_socket, clients)
            else:
                remove_client(client_socket, clients, usernames)
                break
        except:
            remove_client(client_socket, clients, usernames)
            break

def broadcast(message, client_socket, clients):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode("utf-8"))
            except:
                remove_client(client, clients)
                
def remove_client(client_socket, clients, usernames):
    if client_socket in clients:
        clients.remove(client_socket)
        username = usernames[client_socket]
        del usernames[client_socket]
        broadcast(f"{username} has left the chat.", client_socket, clients)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 9999))
    server.listen()

    clients = []
    usernames = {}
    print("Server started and listening for connections...")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection established with {addr}")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, clients, usernames)).start()

if __name__ == "__main__":
    main()
