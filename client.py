import socket
import threading
import os
from colorama import init, Fore, Style
import sys

init()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def receive_messages(client_socket, username):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                sys.stdout.write('\r' + ' ' * (len(username) + 2))
                sys.stdout.write('\r')
                print(f"{Fore.CYAN}{message}{Style.RESET_ALL}")
                sys.stdout.write(f"{Fore.GREEN}{username}: {Style.RESET_ALL}")
                sys.stdout.flush()
            else:
                break
        except:
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 9999))

    clear_screen()
    print(f"{Fore.GREEN}=== Welcome to the Chat Room ==={Style.RESET_ALL}")
    username = input(f"{Fore.YELLOW}Enter your username: {Style.RESET_ALL}")
    client.send(username.encode("utf-8"))
    clear_screen()
    print(f"{Fore.GREEN}=== Chat Room ==={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Type your message and press Enter to send.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Type 'exit' to leave the chat.{Style.RESET_ALL}\n")

    threading.Thread(target=receive_messages, args=(client, username), daemon=True).start()

    while True:
        message = input(f"{Fore.GREEN}{username}: {Style.RESET_ALL}")
        if message.lower() == 'exit':
            break
        client.send(message.encode("utf-8"))

    print(f"\n{Fore.RED}Disconnected from the chat.{Style.RESET_ALL}")
    client.close()

if __name__ == "__main__":
    main()