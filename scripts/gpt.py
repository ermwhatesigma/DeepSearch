from gpt4all import GPT4All
import os

model = GPT4All(model_name="DeepSeek-R1-Distill-Qwen-14B", 
                model_path="D:/deepsearch/models/DeepSeek-R1-Distill-Qwen-14B.gguf", 
                allow_download=False)

os.system('cls' if os.name == 'nt' else 'clear')
print("")
print("    ■■■■      ■■  ")
print("   ■■  ■■         ")
print("  ■■■■■■■■    ■■  ")
print(" ■■      ■■   ■■  ")
print("■■        ■■  ■■  ")
print("\nAI Chatbot (type 'exit' to quit)")
print("anything you ask is AI generated")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Do you hate me?")
        break
    input("Press any key to clear the screen...")
    os.system('cls')

    response = model.generate(user_input, max_tokens=500)
    print(f"AI: {response}\n")