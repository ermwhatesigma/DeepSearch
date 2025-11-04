import socket
import threading
import time
import os

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

os.system('cls')


print("\n-------------------------------------------------------------------------------------------------------------------------------")
print(YELLOW +"■■             ■■  ■■■■■■■  ■■         ■■■■■■    ■■■■■        ■■■   ■■■      ■■■■■■■")
print(" ■■           ■■   ■■       ■■        ■■       ■■     ■■     ■■ ■■ ■■ ■■     ■■     ")
print("  ■■   ■■■   ■■    ■■■■■■■  ■■       ■■        ■■     ■■    ■■   ■■■   ■■    ■■■■■■■")
print("   ■■ ■■ ■■ ■■     ■■       ■■        ■■       ■■     ■■   ■■           ■■   ■■     ")
print("    ■■■   ■■■      ■■■■■■■  ■■■■■■■    ■■■■■■    ■■■■■    ■■             ■■  ■■■■■■■")
print("")
print("■■■■■■■■    ■■■■■")
print("   ■■     ■■     ■■")
print("   ■■     ■■     ■■")
print("   ■■     ■■     ■■")
print("   ■■       ■■■■■")
print("")
print("■■■■■■     ■■■■■■■  ■■■■■■■  ■■■■■■  ")
print("■■   ■■    ■■       ■■       ■■   ■■")
print("■■    ■■   ■■■■■■■  ■■■■■■■  ■■■■■■  ")
print("■■   ■■    ■■       ■■       ■■      ")
print("■■■■■■     ■■■■■■■  ■■■■■■■  ■■      ")
print("                                   ■■■■■   ■■■■■■■      ■■■■      ■■■■■■      ■■■■■■  ■■    ■■  ■■■■■■■  ■■■■■■")
print("                                  ■■       ■■          ■■  ■■     ■■   ■■    ■■       ■■    ■■  ■■       ■■   ■■")
print("                                   ■■■■■   ■■■■■■■    ■■■■■■■■    ■■■■■■    ■■        ■■■■■■■■  ■■■■■■■  ■■■■■■")
print("                                       ■■  ■■        ■■      ■■   ■■   ■■    ■■       ■■    ■■  ■■       ■■   ■■")
print("                                   ■■■■■   ■■■■■■■  ■■        ■■  ■■    ■■    ■■■■■■  ■■    ■■  ■■■■■■■  ■■    ■■" + RESET)
print("\n-------------------------------------------------------------------------------------------------------------------------------")
print(GREEN + "Maker : Sigma")
print("Github : https://github.com/ermwhatesigma" + RESET)
print(GREEN + "\nThis is the port scanner script. It has 3 functions" + RESET)
print("")

open_ports = []

def scan_port(target, port, stop_event):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
                stop_event.set()
    except socket.gaierror:
        print(f"Error: Hostname '{target}' could not be resolved.")
    except Exception as e:
        print(f"Error scanning port {port}: {e}")

def full_port_scan(target):
    stop_event = threading.Event()
    for port in range(1, 65536):
        if stop_event.is_set():
            break
        thread = threading.Thread(target=scan_port, args=(target, port, stop_event))
        thread.start()
    thread.join()

def range_port_scan(target, start_port, end_port):
    stop_event = threading.Event()
    for port in range(start_port, end_port + 1):
        if stop_event.is_set():
            break
        thread = threading.Thread(target=scan_port, args=(target, port, stop_event))
        thread.start()
    thread.join()

def single_port_scan(target):
    stop_event = threading.Event()
    for port in range(1, 65536):
        if stop_event.is_set():
            break
        thread = threading.Thread(target=scan_port, args=(target, port, stop_event))
        thread.start()
    thread.join()

def print_open_ports():
    if open_ports:
        print("Open ports:")
        for port in open_ports:
            print(port)
    else:
        print("No open ports found.")

def main():
    global open_ports
    open_ports = []
    target = input("Enter the target website or IP address (e.g., example.com or 192.168.1.1): ")

    while True:
        print("\nOptions:")
        print("1. Full port scan")
        print("2. Select range of port scan")
        print("3. Single port")
        print("4. Clear screen")
        print("5. QUIT")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            full_port_scan(target)
            print_open_ports()
        elif choice == "2":
            start_port = int(input("Enter the start port: "))
            end_port = int(input("Enter the end port: "))
            range_port_scan(target, start_port, end_port)
            print_open_ports()
        elif choice == "3":
            single_port_scan(target)
            print_open_ports()
        elif choice == '4':
            input("Press any key to clear the screen...")
            os.system('cls' if os.name == 'nt' else 'clear')
        elif choice == "5":
            os.system('cls')
            print(RED + "\n\n\n\n\n\n\n\n\n\n\n\n\nExiting..." + RESET)
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

input("Press any key to clear the screen...")
os.system('cls' if os.name == 'nt' else 'clear')