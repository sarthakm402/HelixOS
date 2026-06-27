import os
import threading
from core.config import ROOT
ROOT = ROOT

_FILE_INDEX = {}
_DIR_INDEX = {}
_LOCK = threading.Lock()


def build_index(root=ROOT):
    new_file_index = {}
    new_dir_index = {}

    for r, dirs, files in os.walk(root):
        for f in files:
            new_file_index[f.lower()] = os.path.join(r, f)

        for d in dirs:
            new_dir_index[d.lower()] = os.path.join(r, d)

    return new_file_index, new_dir_index


def refresh_index(root=ROOT):
    global _FILE_INDEX, _DIR_INDEX

    new_files, new_dirs = build_index(root)

    # atomic swap
    with _LOCK:
        _FILE_INDEX = new_files
        _DIR_INDEX = new_dirs


def get_file_index():
    return _FILE_INDEX


def get_dir_index():
    return _DIR_INDEX