import os
import shutil
from services.file_system import _resolve_file, _resolve_dir
from services.fs_index import refresh_index

def create_file(name, dir=None):
    resolved_dir = _resolve_dir(dir) if dir else os.getcwd()
    if dir and not resolved_dir:
        return {"error": f"directory not found: {dir}"}
    
    final_path = os.path.join(resolved_dir, name)
    with open(final_path, "w", encoding="utf-8") as f:
        pass
    refresh_index()
    return f"created: {final_path}"

def create_dir(name, parent=None):
    resolved_parent = _resolve_dir(parent) if parent else os.getcwd()
    if parent and not resolved_parent:
        return {"error": f"directory not found: {parent}"}
    
    final_path = os.path.join(resolved_parent, name)
    os.makedirs(final_path, exist_ok=True)
    refresh_index()
    return f"created: {final_path}"

def move_file(name, dst_dir):
    resolved_src = _resolve_file(name)
    if not resolved_src:
        return {"error": f"file not found: {name}"}
    resolved_dst = _resolve_dir(dst_dir)
    if not resolved_dst:
        return {"error": f"directory not found: {dst_dir}"}
    
    final = shutil.move(resolved_src, resolved_dst)
    refresh_index()
    return f"moved: {resolved_src} → {final}"

def move_dir(name, dst_dir):
    resolved_src = _resolve_dir(name)
    if not resolved_src:
        return {"error": f"directory not found: {name}"}
    resolved_dst = _resolve_dir(dst_dir)
    if not resolved_dst:
        return {"error": f"directory not found: {dst_dir}"}
    
    final = shutil.move(resolved_src, resolved_dst)
    refresh_index()
    return f"moved: {resolved_src} → {final}"
def delete_file(name):
    resolved = _resolve_file(name)
    if not resolved:
        return {"error": f"file not found: {name}"}
    os.remove(resolved)
    refresh_index()
    return f"deleted: {resolved}"

def delete_dir(name):
    resolved = _resolve_dir(name)
    if not resolved:
        return {"error": f"directory not found: {name}"}
    shutil.rmtree(resolved)
    refresh_index()
    return f"deleted: {resolved}"