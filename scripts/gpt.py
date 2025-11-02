import torch
import time
import os
import threading
from transformers import AutoModelForCausalLM, AutoTokenizer


RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


os.system('cls' if os.name == 'nt' else 'clear')


print("")
print(BLUE +"    ■■■■      ■■  ")
print("   ■■  ■■         ")
print("  ■■■■■■■■    ■■  ")
print(" ■■      ■■   ■■  ")
print("■■        ■■  ■■  " + RESET)
print("\nAI Chatbot (type *exit* to quit)")
print("anything you ask is AI generated")

model_name = "bigscience/bloom-560m"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

user_name = input("What's your name? ").strip()
print(BLUE + f"\nHello {user_name}! Ask me anything. (type *exit* to quit and *clear* to clear the screen)\n" + RESET)

chat_history = "The following is a conversation between a helpful AI and a human.\n\n"


def spinner(stop_event):
    symbols = [RED + '|', '/', '-', '\\' + RESET]
    idx = 0
    while not stop_event.is_set():
        print(RED + f"\rAI is thinking... {symbols[idx % len(symbols)]}" + RESET, end='', flush=True)
        idx += 1
        time.sleep(0.2)
    print("\r" + " " * 40 + "\r", end='')

while True:
    user_input = input(BLUE + f"{user_name}: " + RESET).strip()
    if user_input.lower() in ["*exit*", "*quit*"]:
        print(RED + "AI: DO YOU HATE ME!?\n" + RESET)
        break
    elif user_input.lower() in ["*clear*"]:
        os.system('cls')
        break

    chat_history += f"User: {user_input}\nAI:"

    stop_event = threading.Event()
    t = threading.Thread(target=spinner, args=(stop_event,))
    t.start()

    inputs = tokenizer(chat_history, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.7,
        pad_token_id=tokenizer.eos_token_id
    )

    stop_event.set()
    t.join()

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = decoded.split("AI:")[-1].split(f"{user_name}:")[0].strip()

    print(f"AI: {response}\n")
    chat_history += f" {response}\n"
