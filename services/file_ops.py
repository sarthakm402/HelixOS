import os
import shutil
from services.file_system import _resolve_file, _resolve_dir, _pick
from services.fs_index import refresh_index


def create_file(name, dir=None):
    resolved_dir = _resolve_dir(dir) if dir else os.getcwd()
    if dir and not resolved_dir:
        return {"error": f"directory not found: {dir}"}
    if isinstance(resolved_dir, list):
        resolved_dir = _pick(resolved_dir)
    final_path = os.path.join(resolved_dir, name)
    with open(final_path, "w", encoding="utf-8") as f:
        pass
    refresh_index()
    return f"created: {final_path}"


def create_dir(name, parent=None):
    resolved_parent = _resolve_dir(parent) if parent else os.getcwd()
    if parent and not resolved_parent:
        return {"error": f"directory not found: {parent}"}
    if isinstance(resolved_parent, list):
        resolved_parent = _pick(resolved_parent)
    final_path = os.path.join(resolved_parent, name)
    os.makedirs(final_path, exist_ok=True)
    refresh_index()
    return f"created: {final_path}"


def move_file(name, dst_dir, src_dir=None):
    resolved_src = _resolve_file(name, dir_hint=src_dir)
    if not resolved_src:
        return {"error": f"file not found: {name}"}
    if isinstance(resolved_src, list):
        resolved_src = _pick(resolved_src)

    resolved_dst = _resolve_dir(dst_dir)
    if not resolved_dst:
        return {"error": f"directory not found: {dst_dir}"}
    if isinstance(resolved_dst, list):
        resolved_dst = _pick(resolved_dst)

    final = shutil.move(resolved_src, resolved_dst)
    refresh_index()
    return f"moved: {resolved_src} → {final}"


def move_dir(name, dst_dir, src_dir=None):
    resolved_src = _resolve_dir(name, dir_hint=src_dir)
    if not resolved_src:
        return {"error": f"directory not found: {name}"}
    if isinstance(resolved_src, list):
        resolved_src = _pick(resolved_src)

    resolved_dst = _resolve_dir(dst_dir)
    if not resolved_dst:
        return {"error": f"directory not found: {dst_dir}"}
    if isinstance(resolved_dst, list):
        resolved_dst = _pick(resolved_dst)

    final = shutil.move(resolved_src, resolved_dst)
    refresh_index()
    return f"moved: {resolved_src} → {final}"


def delete_file(name, dir=None):
    resolved = _resolve_file(name, dir_hint=dir)
    if not resolved:
        return {"error": f"file not found: {name}"}
    if isinstance(resolved, list):
        resolved = _pick(resolved)
    os.remove(resolved)
    refresh_index()
    return f"deleted: {resolved}"


def delete_dir(name, dir=None):
    resolved = _resolve_dir(name, dir_hint=dir)
    if not resolved:
        return {"error": f"directory not found: {name}"}
    if isinstance(resolved, list):
        resolved = _pick(resolved)
    shutil.rmtree(resolved)
    refresh_index()
    return f"deleted: {resolved}"