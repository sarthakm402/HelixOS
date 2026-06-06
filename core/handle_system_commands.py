from core.memory import (
    clear_all_history,
    get_all_history,
)
from services.file_system import get_ls,get_pwd,cd
def handle_commands(user_input):
    if user_input == "/exit":
        return "exit"
    if user_input=="/clear":
        clear_all_history()
        print("memory wiped")
        return "command executed"
        
    if user_input=="/history":
        print(get_all_history())
        return "command executed"
    if user_input=="/help":
        print("""
               MODES:
               - Chat mode: anything not starting with "/" goes to AI

              COMMANDS:
              - /help     - show this help menu
              - /history  - show conversation history
              - /clear    - clear current session memory
              - /exit     - close cyberdeck
              -/cd        -change directory
              -/pwd       -current working directory
              -/ls        -list the things present in directory
              USAGE:
              - Type normally to talk to AI
              - Use "/" for system commands

            """)
        return "command executed"
    if user_input=="/pwd":
        
        print(get_pwd())
        return "command executed"
    if user_input=="/cd":
        path=input("pass the path:")
        print(cd(path))
        return "command executed"
    if user_input=="/ls":
        path=input("pass the path:")
        print(get_ls(path))
        return "command executed"        
        