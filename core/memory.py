import json
import os

all_in_memory_history=[]
NOTES_FILE = "/home/sarthak/ml_code_new/HelixOS/notes.json"
def add_message(message: dict,note=False):
    all_in_memory_history.append(message)
    if note:
        if os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, "r") as f:
                notes = json.load(f)
        else:
            notes = []
        notes.append(message)
        with open(NOTES_FILE, "w") as f:
            json.dump(notes, f, indent=2)
def get_all_history():
    return all_in_memory_history
def clear_all_history():
    all_in_memory_history.clear()
    return True
