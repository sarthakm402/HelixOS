from core.chat import ask
print("""
==================================
      AI CYBERDECK v0.1
==================================
""")
while True:
    user_input = input("user> ")
    if user_input == "wq":
        break
    print("Helix> ", end="")
    for token in ask(user_input):
        print(token, end="", flush=True)
    print()