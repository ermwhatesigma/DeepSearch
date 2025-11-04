import os
import subprocess


RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def run_script(script_name):
    subprocess.run(['python', script_name])

os.system('cls' if os.name == 'nt' else 'clear')

while True:
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
    print("\n1. Deep search a name")
    print("2. Phone number and email scraper **note** : That it might work but give the wrong number or email")
    print(RED + "3. DDoS attacker You need an port for it to function" + RESET)
    print("4. Port scanner for websites")
    print(BLUE + "5. This is a script that tries to find active google meets calls for troling **slow**" + RESET)
    print("6. AI chat. All the conted generated after selecting this choice is AI generated. It is still experimental so it might not work.")
    print("7. Exit")

    choice = input("Choose an option (1-7): ")

    if choice == '1':
        run_script('scripts\\name.py')
    elif choice == '2':
        run_script('scripts\\phone-email.py')
    elif choice == '3':
        run_script('scripts\\DDoS.py')
    elif choice == '4':
        run_script('scripts\\port.py')
    elif choice == '5':
        run_script('scripts\\googlemeet.py')
    elif choice == '6':
        run_script('scripts\\gpt.py')
    elif choice == '7':
        run_script('scripts\\clear.py')
        print("WHY DID YOU LEAVE?")
        quit()