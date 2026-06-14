import os 
def get_pwd():
   return os.getcwd()
def get_ls(path="."):
    print(os.listdir(path))# this for llm way
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
def find_file(name,start_path=".",search_files=True,search_dir=False):
    matched_files=[]
    matched_dirs=[]
    for root,dirs,files in os.walk(start_path):
        if search_files:
         if name in files:
             matched_files.append(os.path.join(root,name))
        if search_dir:
            if name in dirs:
                matched_dirs.append(os.path.join(root,name))
    print({
    "matched_files": matched_files,
    "matched_dirs": matched_dirs
})

    return "provided the files"
    