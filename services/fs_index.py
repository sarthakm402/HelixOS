import os
import threading
from core.config import ROOT

_FILE_INDEX = {}
_DIR_INDEX = {}
_LOCK = threading.Lock()


def build_index(root=ROOT):
    new_file_index = {}
    new_dir_index = {}

    for r, dirs, files in os.walk(root):
        for f in files:
            new_file_index.setdefault(f.lower(), []).append(os.path.join(r, f))
        for d in dirs:
            new_dir_index.setdefault(d.lower(), []).append(os.path.join(r, d))

    return new_file_index, new_dir_index


def refresh_index(root=ROOT):
    global _FILE_INDEX, _DIR_INDEX
    new_files, new_dirs = build_index(root)
    with _LOCK:
        _FILE_INDEX = new_files
        _DIR_INDEX = new_dirs


def get_file_index():
    with _LOCK:
        return dict(_FILE_INDEX)


def get_dir_index():
    with _LOCK:
        return dict(_DIR_INDEX)