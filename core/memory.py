import json
all_in_memory_history=[]
def add_usrmsg_to_history(message:dict):
    all_in_memory_history.append(message)
def add_agtmsg_to_history(message:dict):
    all_in_memory_history.append(message)
def get_all_history():
    return all_in_memory_history
def clear_all_history():
    return all_in_memory_history.clear()
