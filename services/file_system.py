import os
from services.fs_index import get_file_index, get_dir_index
def find_file(name):
    if not name:
        return None

    name = name.lower()
    FILE_INDEX = get_file_index()
    if name in FILE_INDEX:
        return FILE_INDEX[name]
    matches = [
        v for k, v in FILE_INDEX.items()
        if name == k
    ]

    return matches[0] if matches else None
def find_dir(name):
    if not name:
        return None
    name = name.lower()
    DIR_INDEX=get_dir_index()
    if name in DIR_INDEX:
        return DIR_INDEX[name]
    matches = [
        v for k, v in DIR_INDEX.items()
        if name == k
    ]
    return matches[0] if matches else None
def get_pwd():
    return os.getcwd()
def read_file(path):
    path = _resolve_file(path)

    if not path:
        return {"error": "File not found"}

    with open(path, "r", encoding="utf-8") as f:
        return f.read()
def get_ls(path="."):
    path = _resolve_dir(path)

    if not path:
        return {"error": "Directory not found"}

    return os.listdir(path)
def cd(path="."):
    path = _resolve_dir(path)

    if not path:
        return {"error": "Directory not found"}

    os.chdir(path)
    return os.getcwd()
def _resolve_file(path):
    if os.path.isfile(path):
        return path
    candidate = find_file(path)
    if candidate and os.path.isfile(candidate):
        return candidate
    return None

def _resolve_dir(path):
    if os.path.isdir(path):
        return path

    candidate = find_dir(path)
    if candidate and os.path.isdir(candidate):
        return candidate

    return None