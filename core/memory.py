import json
import os

all_in_memory_history=[]
NOTES_FILE = "/home/sarthak/ml_code_new/HelixOS/notes.json"
def add_message(message: dict):
    all_in_memory_history.append(message)
def get_all_history():
    return all_in_memory_history
def clear_all_history():
    all_in_memory_history.clear()
    return True
def remember(fact):
    try:
        with open(NOTES_FILE, "r") as f:
            memories = json.load(f)
    except (
        FileNotFoundError,
        json.JSONDecodeError
    ):
        memories = []
    memories.append(fact)
    with open(NOTES_FILE, "w") as f:
        json.dump(
            memories,
            f,
            indent=2
        )
    return "memory stored"
def get_memories():
    if not os.path.exists(NOTES_FILE):
        return []
    try:
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []