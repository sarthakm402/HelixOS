import os
from services.llm import create_summary
from services.ast_helper import parse_python_metadata
from core.config import SUPPORTED_FILE_EXTENSIONS
def list_files(file_names=None, start_path="."):
    matched_files = []
    file_ext =SUPPORTED_FILE_EXTENSIONS

    for root, dirs, files in os.walk(start_path):
        # specific files
        if file_names:
            for file in file_names:
                if file in files:
                    matched_files.append(os.path.join(root, file))
        #scan all relevant files
        else:
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext in file_ext:
                    matched_files.append(os.path.join(root, file))
    return matched_files


def create_snapshot(files: list):
    txt_snap = {}
    md_snap = {}
    code_snap = {}      

    for filepath in files:
        ext = os.path.splitext(filepath)[1]   

        try:
            with open(filepath, "r", encoding="utf-8") as f:  
                content = f.read()
        except (OSError, UnicodeDecodeError):
            continue        
        if ext == ".txt":
            txt_snap[filepath] = content
        elif ext == ".md":
            md_snap[filepath] = content
        elif ext in {".py", ".ipynb"}:
            code_snap[filepath]=parse_python_metadata(content)
    repo_info={
        "txt_snapshot":txt_snap,
        "readme_snapshot":md_snap,
        "code_files":code_snap
    }
    return repo_info
def summary(repo_info:dict):
    return create_summary(repo_info)

            

