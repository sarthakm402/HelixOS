import os 
def get_pwd():
    os.getcwd()
def get_ls(path="."):
    return os.listdir(path)
def cd(path):
    os.chdir(path)
    return os.getcwd()
    