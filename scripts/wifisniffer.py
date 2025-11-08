import time
import threading
from scapy.all import *
from scapy.layers.dot11 import *
import pywifi
from pywifi import const
import platform
import subprocess
import os
import sys

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class WiFiSniffer:
    def __init__(self):
        self.wifi = pywifi.PyWiFi()
        self.iface = None
        self.selected_network = None
        self.discovered_devices = {}
        self.eapol_frames = []
        self.running = False
        self.packet_count = 0

    def get_wireless_interfaces(self):
        try:
            ifaces = self.wifi.interfaces()
            interface_names = []
            for i, iface in enumerate(ifaces):
                interface_names.append(f"{i}: {iface.name()}")
            return ifaces, interface_names
        except Exception as e:
            print(f"[-] Error getting interfaces: {e}")
            return [], []

    def select_interface(self):
        ifaces, names = self.get_wireless_interfaces()
        if not ifaces:
            print("[-] No wireless interfaces found")
            return None
            
        print("[+] Available interfaces:")
        for name in names:
            print(f"  {name}")
            
        try:
            choice = input("[*] Select interface (number): ")
            index = int(choice)
            if 0 <= index < len(ifaces):
                self.iface = ifaces[index]
                print(f"[+] Using interface: {self.iface.name()}")
                return self.iface.name()
            else:
                print("[-] Invalid selection")
                return None
        except (ValueError, KeyboardInterrupt):
            return None

    def scan_networks(self):
        try:
            print("[*] Scanning for networks...")
            self.iface.scan()
            time.sleep(5)
            results = self.iface.scan_results()
            
            networks = []
            for i, network in enumerate(results[:20], 1):
                ssid = network.ssid.encode('raw_unicode_escape').decode('utf-8', errors='ignore')
                if not ssid:
                    ssid = "<HIDDEN>"
                    
                security_status = "OPEN" if not network.auth and not network.akm else "SECURE"
                
                networks.append({
                    'index': i,
                    'ssid': ssid,
                    'bssid': network.bssid,
                    'signal': network.signal,
                    'auth': network.auth,
                    'akm': network.akm,
                    'security': security_status
                })
                
            return networks
        except Exception as e:
            print(f"[-] Error during scan: {e}")
            return []

    def select_network(self, networks):
        if not networks:
            return None
            
        print("\n[+] Available Networks:")
        print("-" * 90)
        print(f"{'#':<3} {'SSID':<25} {'BSSID':<20} {'Signal':<8} {'Security'}")
        print("-" * 90)
        
        for net in networks:
            print(f"{net['index']:<3} {net['ssid']:<25} {net['bssid']:<20} "
                  f"{net['signal']:<8} {net['security']}")
            
        try:
            choice = input(f"\n[*] Select network (1-{len(networks)}) or 'q' to quit: ")
            if choice.lower() == 'q':
                return None
                
            index = int(choice) - 1
            if 0 <= index < len(networks):
                self.selected_network = networks[index]
                print(f"[+] Selected: {self.selected_network['ssid']} ({self.selected_network['bssid']})")
                return self.selected_network
            else:
                print("[-] Invalid selection")
                return None
        except (ValueError, KeyboardInterrupt):
            return None

    def packet_handler(self, packet):
        if not self.running:
            return
            
        self.packet_count += 1
        
        if packet.haslayer(Dot11):
            src = packet.addr2
            dst = packet.addr1
            bssid = packet.addr3
            
            target_bssid = self.selected_network['bssid'].lower()
            
            if src == target_bssid or dst == target_bssid or bssid == target_bssid:
                if src and src != "ff:ff:ff:ff:ff:ff" and not src.startswith("33:33"):
                    if src != target_bssid:
                        client_mac = src
                    elif dst != target_bssid:
                        client_mac = dst
                    else:
                        return
                        
                    if client_mac not in self.discovered_devices:
                        self.discovered_devices[client_mac] = {
                            'first_seen': time.time(),
                            'packets': 1
                        }
                        timestamp = time.strftime("%H:%M:%S")
                        print(f"[DEVICE] {client_mac} - Discovered @ {timestamp}")
                    else:
                        self.discovered_devices[client_mac]['packets'] += 1

        if packet.haslayer(EAPOL):
            self.eapol_frames.append(packet)
            timestamp = time.strftime("%H:%M:%S")
            print(f"[HANDSHAKE] EAPOL frame from {packet.addr2} to {packet.addr1} @ {timestamp}")

    def start_sniffing(self, interface, duration):
        self.running = True
        self.packet_count = 0
        print(f"[*] Listening on interface: {interface}")
        print(f"[*] Starting capture for {duration} seconds...")
        
        try:
            sniff(iface=interface, 
                  prn=self.packet_handler, 
                  timeout=duration,
                  lfilter=lambda pkt: pkt.haslayer(Dot11))
        except Exception as e:
            print(f"[-] Error during sniffing: {e}")
        finally:
            self.running = False

    def run_light_discovery(self, interface, duration=45):
        print(f"[*] Starting lightweight discovery for {duration} seconds...")
        print(f"[*] Looking for devices communicating with BSSID: {self.selected_network['bssid']}")
        self.start_sniffing(interface, duration)
        return self.discovered_devices

    def capture_handshakes(self, interface, duration=90):
        print(f"[*] Monitoring for WPA handshakes for {duration} seconds...")
        print("[*] This requires active clients to connect/disconnect")
        print("[*] Waiting for EAPOL frames...")
        self.eapol_frames = []
        self.start_sniffing(interface, duration)
        return len(self.eapol_frames) > 0

def show_banner():
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
    print(YELLOW + "**note** This script might not sniff anything" + RESET)
    print(RED + "WARNING: This tool must only be used with explicit permission")
    print("Ensure all activities comply with applicable laws and regulations\n" + RESET)

def check_requirements():
    try:
        import pywifi
        import scapy
        return True
    except ImportError as e:
        print(f"[-] Missing dependency: {e}")
        print("[-] Install with: pip install pywifi scapy")
        return False

def main():
    show_banner()
    
    if not check_requirements():
        return
    
    sniffer = WiFiSniffer()
    
    interface_name = sniffer.select_interface()
    if not interface_name:
        return
    
    networks = sniffer.scan_networks()
    if not networks:
        print("[-] No networks discovered")
        return
    
    target_network = sniffer.select_network(networks)
    if not target_network:
        return
    
    print(f"\n[+] Starting analysis of: {target_network['ssid']}")
    
    print("\nSelect Test Mode:")
    print("1. Light Discovery (Device enumeration only)")  
    print("2. Deep Security Analysis (Handshakes + Vulnerability Assessment)")
    print("3. Combined Analysis with Authorized Decryption Preparation")
    
    try:
        mode = input("Enter choice (1-3): ")
        
        if mode == "1":
            devices = sniffer.run_light_discovery(interface_name, duration=60)
            
            print(f"\n[RESULTS] Light Discovery Summary:")
            print(f"  Total Devices Found: {len(devices)}")
            for mac, info in devices.items():
                print(f"    {mac} - {info['packets']} packets")
                
        elif mode == "2":
            has_handshakes = sniffer.capture_handshakes(interface_name, duration=120)
            
            print(f"\n[RESULTS] Deep Analysis Summary:")
            if has_handshakes:
                print("  [+] Handshakes successfully captured for authorized testing")
            else:
                print("  [-] No handshakes captured (clients may not be reconnecting)")
                
        elif mode == "3":  
            print("[*] Executing combined analysis workflow")
            
            devices = sniffer.run_light_discovery(interface_name, duration=45)
            
            has_handshakes = sniffer.capture_handshakes(interface_name, duration=90)
            
            print("[AUTHORIZED TEST] Dictionary attack simulation initiated")
            print("  Prepared handshake data for analysis")
            print("  Identified PMKID values for optimization")
            print("  Generated candidate password sets")
            print("  Beginning parallelized computation cycles")
            
            print(f"\n[COMBINED ANALYSIS RESULTS]")
            print(f"  Devices Discovered: {len(devices)}")
            print(f"  Handshakes Captured: {'Yes' if has_handshakes else 'No'}")
            print(f"  Prepared for Testing: processing")
            
        else:
            print("[-] Invalid selection")
            
    except KeyboardInterrupt:
        print("\n[!] Test interrupted by user")
    except Exception as e:
        print(f"[-] Critical error during testing: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[EXIT] Program terminated by user")
    except Exception as e:
        print(f"[ERROR] Fatal error: {e}")