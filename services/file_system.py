import os 
def get_pwd():
   return os.getcwd()
def get_ls(path="."):
    return os.listdir(path)
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