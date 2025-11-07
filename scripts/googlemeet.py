import requests
import itertools
import string
import threading
import time
import random
import os

os.system('cls' if os.name == 'nt' else 'clear')


RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def start():
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
    print("\n-------------------------------------------------------------------------------------------------------------------------------")
    print(GREEN + "Maker : Sigma")
    print("Github : https://github.com/ermwhatesigma" + RESET)
    print(BLUE + "\nThis script runs inf\nThis is the google meet finder. It tries to find open google meet calls. \n**Remember** it might take long before anything happens. If it does find anything use it only for smart things ;)\n" + RESET)

start()
input("Press any key to start...")
os.system('cls' if os.name == 'nt' else 'clear')
start()


def generate_google_meet_id():
    part1 = ''.join(random.choices(string.ascii_lowercase, k=3))
    part2 = ''.join(random.choices(string.ascii_lowercase, k=4))
    part3 = ''.join(random.choices(string.ascii_lowercase, k=3))
    return f"{part1}-{part2}-{part3}"

def check_google_meet(meet_id):
    meet_url = f"https://meet.google.com/{meet_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    try:
        response = requests.get(meet_url, headers=headers, allow_redirects=True)
        if response.status_code == 200:
            if "Check your connection" not in response.text and "Unable to find meeting" not in response.text and "Meeting not found" not in response.text:
                if "Join now" in response.text or "Join meeting" in response.text or "Ready to join?" in response.text:
                    print(GREEN + f"Found open Google Meet: {meet_url}" + RESET)
                    return True
                else:
                    print(RED + f"Meeting found but not active: {meet_url}" + RESET)
            else:
                print(RED + f"Meeting not found or invalid: {meet_url}" + RESET)
        else:
            print(RED + f"Failed to retrieve meeting page: {meet_url} (Status code: {response.status_code})" + RESET)
    except requests.exceptions.RequestException as e:
        print(RED + f"Request failed: {e}" + RESET)
    return False

def main():
    threads = []
    for _ in range(999):
        meet_id = generate_google_meet_id()
        thread = threading.Thread(target=check_google_meet, args=(meet_id,))
        threads.append(thread)
        thread.start()
        time.sleep(1)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()