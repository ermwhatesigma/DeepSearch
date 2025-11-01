import requests
from bs4 import BeautifulSoup
import re
import time
import os


RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

os.system('cls' if os.name == 'nt' else 'clear')

print("\n-------------------------------------------------------------------------------------------------------------------------------")
print(GREEN +"■■             ■■  ■■■■■■■  ■■         ■■■■■■    ■■■■■        ■■■   ■■■      ■■■■■■■")
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
print("\nThis is the to deep search some ones name")


def search_name(first_name, last_name):
    first_name = first_name.replace(" ", "+")
    last_name = last_name.replace(" ", "+")

    query = f"{first_name}+{last_name}"

    urls = [
        f"https://www.google.com/search?q={query}",
        f"https://www.bing.com/search?q={query}",
        f"https://www.facebook.com/search?q={query}",
        f"https://www.linkedin.com/search/results/people/?keywords={query}",
        f"https://www.instagram.com/explore/tags/{query}/",
        f"https://twitter.com/search?q={query}",
        f"https://www.tiktok.com/search?q={query}",
        f"https://www.pinterest.com/search/pins/?q={query}",
        f"https://itch.io/search?q={query}",
        f"https://www.youtube.com/results?search_query={query}",
        f"https://www.quora.com/search?q={query}",
        f"https://duckduckgo.com/{query}",
        f"https://www.reddit.com/search/?q={query}",
        f"https://search.brave.com/search?q={query}"
    ]

    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    phone_pattern = r'\+?\d[\d -]{8,12}\d'

    results = []
    for url in urls:
        for attempt in range(3):
            try:
                print(f"Attempting to retrieve data from {url}...")
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    for item in soup.find_all(['div', 'span', 'p', 'a']):
                        text = item.get_text()
                        if re.search(email_pattern, text) or re.search(phone_pattern, text):
                            results.append(text)
                    print(GREEN + f"Successfully retrieved data from {url}." + RESET)
                    break 
                else:
                    print(RED + f"Failed to retrieve data from {url}. Status code: {response.status_code}" + RESET)
            except Exception as e:
                print(f"Error accessing {url}: {e}")
            time.sleep(5)

    return results

if __name__ == "__main__":
    first_name = input("Enter the first name: ")
    last_name = input("Enter the last name: ")
    results = search_name(first_name, last_name)
    for result in results:
        print(result)
        break

input("Press any key to clear the screen...")
os.system('cls')   