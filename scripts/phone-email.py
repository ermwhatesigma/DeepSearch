import requests
from bs4 import BeautifulSoup
import re
import time
import os
import brotli

RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

os.system('cls' if os.name == 'nt' else 'clear')

print("\n-------------------------------------------------------------------------------------------------------------------------------")
print(RED +"■■             ■■  ■■■■■■■  ■■         ■■■■■■    ■■■■■        ■■■   ■■■      ■■■■■■■")
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
print(RED+ "\n**note** This script tries to scrape emails and phone numbers form the provided link. \n**REMEMBER** that this script it might give you emails and phone numbers but it might not be the one youve been seaching for." + RESET)
print("")


def extract_phone_number(text):
    phone_pattern = re.compile(
        r'(\+?1[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{4})|'  
        r'(\+?3\d{1,3}[\s\-]?\d{1,4}[\s\-]?\d{2,4}[\s\-]?\d{2,4}[\s\-]?\d{0,4})|'  
        r'(\+?4\d{1,3}[\s\-]?\d{1,4}[\s\-]?\d{2,4}[\s\-]?\d{2,4}[\s\-]?\d{0,4})'
    )
    phone_numbers = phone_pattern.findall(text)
    flat_numbers = [num for group in phone_numbers for num in group if num]
    return flat_numbers

def extract_email(text):
    words = text.split()
    emails = [word for word in words if '@' in word]
    return emails

def scrape_website(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        if response.headers.get("Content-Encoding") == "br":
            html = brotli.decompress(response.content).decode("utf-8")
        else:
            html = response.text
        try:
            import lxml
        except ImportError:
            return [], []
        soup = BeautifulSoup(html, "lxml")
        text = soup.get_text()
        phone_numbers = extract_phone_number(text)
        emails = extract_email(text)
        return phone_numbers, emails
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return [], []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return [], []

def main():
    url = input("Enter the URL to scrape: ")
    phone_numbers, emails = scrape_website(url)
    if phone_numbers:
        print("Found phone numbers:")
        for number in phone_numbers:
            print(number)
    else:
        print("No phone numbers found.")
    if emails:
        print("Found emails:")
        for email in emails:
            print(email)
    else:
        print("No emails found.")

if __name__ == "__main__":
    main()

input("Press any key to clear the screen...")
os.system('cls' if os.name == 'nt' else 'clear')