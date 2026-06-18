import os 
def get_pwd():
   return os.getcwd()
def _resolve_file(path):
    if os.path.isfile(path):
        return path
    return find_file(path)
def _resolve_dir(path):
    if os.path.isdir(path):
        return path
    return find_dir(path)
def read_file(path):
    path = _resolve_file(path)
    if not path or "not found" in path.lower():
        return "File not found"
    with open(path, "r") as f:
        return f.read()
def get_ls(path="."):
    path = _resolve_dir(path)
    if not path or "not found" in path.lower():
        return "Directory not found"
    return os.listdir(path)
def cd(path="."):
    path = _resolve_dir(path)
    if not path or "not found" in path.lower():
        return "Directory not found"
    os.chdir(path)
    return os.getcwd()
def find_file(
    name,
    start_path="/home/sarthak",
):
    matched_files = []
    target = name.lower()
    for root, dirs, files in os.walk(start_path):
            for file in files:
                if file.lower() == target:          # exact match first
                    matched_files.insert(0, os.path.join(root, file))
                elif target in file.lower():         # partial match after
                    matched_files.append(os.path.join(root, file))
    return matched_files[0] if matched_files else []
def find_dir(
    name,
    start_path="/home/sarthak",
):
    matched_dirs = []
    target = name.lower()
    for root, dirs, files in os.walk(start_path):
            for dir in dirs:
                if dir.lower() == target:          # exact match first
                    matched_dirs.insert(0, os.path.join(root, dir))
                elif target in dir.lower():         # partial match after
                    matched_dirs.append(os.path.join(root, dir))
    return matched_dirs[0] if matched_dirs else []