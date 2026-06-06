import json
from core.memory import add_message
from core.router import route_user_input
print(""" ================================== AI CYBERDECK v0.1 ================================== """)
while True:
    user_input = input("user> ")
    result=route_user_input(user_input)
    if result== "exit":
        break
    if result=="command executed":
        continue
    add_message({
        "role": "user",
        "content": user_input
    })
    print("Helix> ", end="")
    assistant_response = ""
    for token in result:
        print(token, end="", flush=True)
        assistant_response += token
    print()
    add_message({
        "role": "assistant",
        "content": assistant_response
    })