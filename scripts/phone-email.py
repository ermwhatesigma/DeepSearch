import requests
from bs4 import BeautifulSoup
import re
import time
import os

RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

os.system('cls')

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
print(RED+ "\nThis is the deepseacrh of a website. It tries to scrape email or phone number from the provided link of an user. \n**note** This scraper needs chrome driver to work. it tries to look at all the emails and phone numbers in a page. \n**disclaimer** This might give you emails or phone numbers. But note that it might not give the details of the person you where searching for." + RESET)
print("")


def extract_phone_number(text):
    phone_pattern = re.compile(r'\+?\d[\d -]{7,}\d')
    phone_numbers = phone_pattern.findall(text)
    return phone_numbers

def extract_email(text):
    email_pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
    emails = email_pattern.findall(text)
    return emails

def scrape_website(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        try:
            import lxml
        except ImportError:
            print("The lxml package is not installed. Run: pip install lxml")
            return [], []
        soup = BeautifulSoup(response.text, "lxml")

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
os.system('cls')