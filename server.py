import socket
import argparse
import threading
from colorama import Fore, Style
from pyfiglet import Figlet

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-i", "--ip", help="Server IP address", default="127.0.0.1")
arg_parser.add_argument("-p", "--port", help="Server port", type=int, default=1234)

def handle_client(client_socket, address):
    print(f"{Fore.GREEN}[+] Accepted connection from {address}{Style.RESET_ALL}")

    try:
        while True:
            command = input(f"{Fore.YELLOW}Enter command (type 'exit' to close connection): {Style.RESET_ALL}")
            client_socket.send(command.encode())

            if command.lower() == "exit":
                break

            result = client_socket.recv(1024).decode()
            print(f"{Fore.CYAN}Result from {address}: {result}{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}Error with {address}: {str(e)}{Style.RESET_ALL}")

    finally:
        client_socket.close()
        print(f"{Fore.YELLOW}[-] Connection with {address} closed{Style.RESET_ALL}")

def print_heading():
    f = Figlet(font="slant")
    heading = f.renderText("Server Script")
    print(f"{Fore.BLUE}{Style.BRIGHT}{heading}{Style.RESET_ALL}")

def main():
    args = arg_parser.parse_args()
    ip = args.ip
    port = args.port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(5)

    print_heading()
    print(f"{Fore.GREEN}[+] Server listening on {ip}:{port}{Style.RESET_ALL}")

    try:
        while True:
            client_socket, address = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
            client_handler.start()

    except KeyboardInterrupt:
        print(f"{Fore.RED}\n[+] Server shutting down...{Style.RESET_ALL}")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
