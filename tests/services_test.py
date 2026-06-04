from core.chat import ask
user_input = input("Please enter your query: ")
for token in ask(user_input):
    print(token, end="", flush=True)


