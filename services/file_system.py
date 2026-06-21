import os
import services.fs_index as fs_index
def find_file(name):
    if not name:
        return None

    name = name.lower()
    if name in fs_index.FILE_INDEX:
        return fs_index.FILE_INDEX[name]
    matches = [
        v for k, v in fs_index.FILE_INDEX.items()
        if name in k
    ]

    return matches[0] if matches else None
def find_dir(name):
    if not name:
        return None
    name = name.lower()
    if name in fs_index.DIR_INDEX:
        return fs_index.DIR_INDEX[name]
    matches = [
        v for k, v in fs_index.DIR_INDEX.items()
        if name in k
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
    return find_file(path)


def _resolve_dir(path):
    if os.path.isdir(path):
        return path
    return find_dir(path)