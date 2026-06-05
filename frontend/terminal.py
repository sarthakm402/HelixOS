import json
from core.chat import ask
from core.memory import add_message,clear_all_history,get_all_history
print(""" ================================== AI CYBERDECK v0.1 ================================== """)
while True:
    user_input = input("user> ")
    if user_input == "/exit":
        break
    if user_input=="/clear":
        clear_all_history()
        print("history cleared")
        continue
    if user_input=="/history":
        print(get_all_history())
        continue
    if user_input=="/help":
        print("""
               MODES:
               - Chat mode: anything not starting with "/" goes to AI

              COMMANDS:
              - /help     - show this help menu
              - /history  - show conversation history
              - /clear    - clear current session memory
              - /exit     - close cyberdeck
              USAGE:
              - Type normally to talk to AI
              - Use "/" for system commands

            """)
        continue
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