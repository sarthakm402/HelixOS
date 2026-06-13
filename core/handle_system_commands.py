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
              -/read_file -read the content of the files provided
              -/find      -helps to find file or directory
              -/analyse   -helps to give prelim analysis of a repo
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
        if not path or path=='':
            print("no path provided")
            path="."
        print(cd(path))
        return "command executed"
    if user_input=="/ls":  
        path=input("pass the path:")
        if not path or path=='':
            print("no path provided")
            path="."
        print(get_ls(path))
        return "command executed"   
    if user_input=="/read_file":
        path=input("pass the path:")
        print(read_file(path))
        return "command executed"  
    if user_input=="/find":
        name=input("enter the name of file or directory:")
        path=input("pass the path:")
        if not path or path=="":
            print("path not provided")
            path="."
        print(find_file(name,path))
        return "command executed"
    if user_input=="/analyse":
        files_given=input("give names of files to be analysed:")
        files = list_files(files_given)
        repo_info = create_snapshot(files)
        full_summary = summary(repo_info)
        print(full_summary)
        return "command executed" 
    if user_input=="/remember":
        fact = user_input.replace(
        "/remember",
        "",
        1
    ).strip()
    remember({
        "fact": fact
    })

    return "command executed"




    
 
        