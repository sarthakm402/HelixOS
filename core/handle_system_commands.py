from core.memory import clear_all_history, get_all_history

def handle_commands(user_input):
    if user_input == "/exit":
        return "exit"

    if user_input == "/help":
        print("""...""")
        return "command executed"

    if user_input == "/history":
        history = get_all_history()
        print(history)
        return "command executed"

    if user_input == "/clear":
        clear_all_history()
        print("memory cleared")
        return "command executed"

    print(f"unknown command: {user_input} (try /help)")
    return "command executed"