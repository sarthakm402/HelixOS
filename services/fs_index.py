import os 
FILE_INDEX = {}
DIR_INDEX = {}
ROOT = "/home/sarthak"
def build_index(root=ROOT):
    """
    Build in-memory filesystem index.
    Call once at startup.
    """
    FILE_INDEX.clear()
    DIR_INDEX.clear()
    for r, dirs, files in os.walk(root):
        for f in files:
            FILE_INDEX[f.lower()] = os.path.join(r, f)
        for d in dirs:
            DIR_INDEX[d.lower()] = os.path.join(r, d)
def refresh_index():
    return build_index(ROOT)
