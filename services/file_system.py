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


def _filter_by_dir_hint(matches, dir_hint):
    if not dir_hint:
        return matches
    dir_hint = dir_hint.lower()
    filtered = [p for p in matches if dir_hint in p.replace("\\", "/").lower()]
    return filtered if filtered else matches


def _pick(candidates):
    """Returns a chosen path, or None if selection fails/cancelled."""
    for i, c in enumerate(candidates, 1):
        print(f"  {i}. {c}")
    choice = input("select the path (or blank to cancel): ").strip()
    if not choice:
        return None
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(candidates):
            return candidates[idx]
        return None
    except ValueError:
        return None


def _resolve_file(path, dir_hint=None):
    candidate = find_file(path)
    if isinstance(candidate, list):
        candidate = _filter_by_dir_hint(candidate, dir_hint)
        if len(candidate) == 1:
            return candidate[0]
        return candidate
    if candidate and os.path.isfile(candidate):
        return candidate
    if os.path.isfile(path):
        return path
    return None


def _resolve_dir(path, dir_hint=None):
    candidate = find_dir(path)
    if isinstance(candidate, list):
        candidate = _filter_by_dir_hint(candidate, dir_hint)
        if len(candidate) == 1:
            return candidate[0]
        return candidate
    if candidate and os.path.isdir(candidate):
        return candidate
    if os.path.isdir(path):
        return path
    return None


def get_pwd():
    return os.getcwd()


def read_file(path, dir=None):
    resolved = _resolve_file(path, dir_hint=dir)
    if resolved is None:
        return {"error": f"file not found: {path}"}
    if isinstance(resolved, list):
        resolved = _pick(resolved)
        if resolved is None:
            return {"error": "no file selected"}
    try:
        with open(resolved, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        return {"error": f"cannot read '{resolved}' — not a text file"}
    except IsADirectoryError:
        return {"error": f"'{resolved}' is a directory, not a file"}
    except PermissionError:
        return {"error": f"permission denied reading '{resolved}'"}
    except OSError as e:
        return {"error": f"could not read '{resolved}': {e}"}


def get_ls(path=".", dir=None):
    resolved = _resolve_dir(path, dir_hint=dir)
    if resolved is None:
        return {"error": f"directory not found: {path}"}
    if isinstance(resolved, list):
        resolved = _pick(resolved)
        if resolved is None:
            return {"error": "no directory selected"}
    try:
        return os.listdir(resolved)
    except PermissionError:
        return {"error": f"permission denied listing '{resolved}'"}
    except OSError as e:
        return {"error": f"could not list '{resolved}': {e}"}


def cd(path=".", dir=None):
    resolved = _resolve_dir(path, dir_hint=dir)
    if resolved is None:
        return {"error": f"directory not found: {path}"}
    if isinstance(resolved, list):
        resolved = _pick(resolved)
        if resolved is None:
            return {"error": "no directory selected"}
    try:
        os.chdir(resolved)
        return os.getcwd()
    except (PermissionError, FileNotFoundError) as e:
        return {"error": f"could not change directory to '{resolved}': {e}"}