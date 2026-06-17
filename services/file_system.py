import os 
def get_pwd():
   return os.getcwd()
def get_ls(path="."):
    return os.listdir(path)#this for handle commands 
def cd(path="."):
    if not os.path.exists(path):
        return "Directory not found"
    if not os.path.isdir(path):
        return "Not a directory"
    os.chdir(path)
    return os.getcwd()
def read_file(path):
    if not os.path.exists(path):
        return "File not found"
    if not os.path.isfile(path):
        return "Not a file"
    with open(path,"r") as f:
        content=f.read()
    return content
def find_file_or_folder(
    name,
    start_path="/home/sarthak",
    search_files=True,
    search_dir=True
):
    matched_files = []
    matched_dirs = []
    target = name.lower()
    for root, dirs, files in os.walk(start_path):
        if search_files:
            for file in files:
                if file.lower() == target:          # exact match first
                    matched_files.insert(0, os.path.join(root, file))
                elif target in file.lower():         # partial match after
                    matched_files.append(os.path.join(root, file))
        if search_dir:
            for directory in dirs:
                if directory.lower() == target:
                    matched_dirs.insert(0, os.path.join(root, directory))
                elif target in directory.lower():
                    matched_dirs.append(os.path.join(root, directory))
    return {
        "matched_files": matched_files[0] if matched_files else [],
        "matched_dirs": matched_dirs[0] if matched_dirs else []
    }