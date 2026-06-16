from core.memory import (
    clear_all_history,
    get_all_history,
    remember
)
from services.file_system import get_ls,get_pwd,cd,read_file,find_file

from core.analyser import list_files,create_snapshot,summary
def handle_commands(user_input):
    if user_input == "/exit":
        return "exit"
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
              -/read_file -read the content of the files provided
              -/find      -helps to find file or directory
              -/analyse   -helps to give prelim analysis of a repo
              USAGE:
              - Type normally to talk to AI
              - Use "/" for system commands

            """)
        return "command executed"



    
 
        