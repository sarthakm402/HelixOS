import os
from services.fs_index import get_file_index, get_dir_index


def find_file(name):
    if not name:
        return None

    name = name.lower()
    FILE_INDEX = get_file_index()

    matches = FILE_INDEX.get(name, [])
    if not matches:
        return None
    if len(matches) == 1:
        return matches[0]
    return matches


def find_dir(name):
    if not name:
        return None

    name = name.lower()
    DIR_INDEX = get_dir_index()

    matches = DIR_INDEX.get(name, [])
    if not matches:
        return None
    if len(matches) == 1:
        return matches[0]
    return matches


def get_pwd():
    return os.getcwd()
def _pick(candidates):
    for i, c in enumerate(candidates, 1):
        print(f"  {i}. {c}")
    choice = input("select the path: ")
    return candidates[int(choice) - 1]
def read_file(path):
    resolved = _resolve_file(path)
    
    if resolved is None:
        return {"error": "File not found"}
    if isinstance(resolved, list):
        resolved=_pick(candidates=resolved)#so if 1 written we go to 0
    with open(resolved, "r", encoding="utf-8") as f:
        return f.read()


def get_ls(path="."):
    resolved = _resolve_dir(path)

    if resolved is None:
        return {"error": "Directory not found"}
    if isinstance(resolved, list):
        resolved=_pick(resolved)

    return os.listdir(resolved)


def cd(path="."):
    resolved = _resolve_dir(path)

    if resolved is None:
        return {"error": "Directory not found"}
    if isinstance(resolved, list):
        resolved=_pick(resolved)

    os.chdir(resolved)
    return os.getcwd()


def _resolve_file(path):
   

    candidate = find_file(path)
    if isinstance(candidate, list):
        return candidate
    if candidate and os.path.isfile(candidate):
        return candidate
    if os.path.isfile(path):
        return path
    return None


def _resolve_dir(path):
 

    candidate = find_dir(path)
    if isinstance(candidate, list):
        return candidate
    if candidate and os.path.isdir(candidate):
        return candidate
    if os.path.isdir(path):
        return path
    return None