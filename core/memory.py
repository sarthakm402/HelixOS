import json
all_in_memory_history=[]
def add_message(message: dict):
    all_in_memory_history.append(message)
def get_all_history():
    return all_in_memory_history
def clear_all_history():
    return all_in_memory_history.clear()
