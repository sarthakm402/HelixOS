import psutil
import subprocess
import psutil
from services.platform import run_shell as _platform_run_shell,get_system_stats,run_python_module as _platform_run_python_module
import os
from services.file_system import _pick,_resolve_file,cd,_resolve_dir
from core.config import PROJECT_ROOT
def get_system_usage():
    return get_system_stats()
def list_processes(filter_name=None):
    procs = []
    for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_info"]):
        try:
            info = p.info
            if filter_name and filter_name.lower() not in info["name"].lower():
                continue
            procs.append({
                "pid": info["pid"],
                "name": info["name"],
                "cpu": info["cpu_percent"],
                "ram_mb": round(info["memory_info"].rss / 1e6, 1),
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return sorted(procs, key=lambda x: x["cpu"], reverse=True)[:20]


def kill_process(name=None, pid=None):
    if pid:
        targets = [{"pid": pid}]
    elif name:
        targets = list_processes(filter_name=name)
    else:
        return {"error": "provide either name or pid"}

    killed = []

    for proc in targets:
        try:
            p = psutil.Process(proc["pid"])
            pname = p.name()
            p.terminate()
            killed.append(f"{pname} (pid {proc['pid']})")
        except psutil.NoSuchProcess:
            continue
        except psutil.AccessDenied:
            continue

    if not killed:
        return {"error": "no matching process found"}

    return f"terminated: {', '.join(killed)}"

def run_shell(command, timeout=10):
   return _platform_run_shell(command,timeout=timeout)

def run_python_module(name, dir=None, args=None, cwd=None):
    resolved_file = _resolve_file(name, dir_hint=dir)
    if not resolved_file:
        return {"error": f"could not find file: {name}"}
    if isinstance(resolved_file, list):
        resolved_file = _pick(resolved_file)

    # working directory: explicit cwd hint > the file's own containing directory
    if cwd:
        resolved_root = _resolve_dir(cwd)
        if not resolved_root:
            return {"error": f"could not find project root: {cwd}"}
        if isinstance(resolved_root, list):
            resolved_root = _pick(resolved_root)
    else:
        resolved_root = os.path.dirname(resolved_file)

    return _platform_run_python_module(resolved_file, args, resolved_root)