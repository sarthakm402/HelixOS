import json
from core.chat import ask
from core.memory import add_message
while True:
    user_input = input("user> ")
    if user_input == "wq":
        break
    add_message({
        "role": "user",
        "content": user_input
    })
    print("Helix> ", end="")
    assistant_response = ""
    for token in ask(user_input):
        print(token, end="", flush=True)
        assistant_response += token
    print()
    add_message({
        "role": "assistant",
        "content": assistant_response
    })