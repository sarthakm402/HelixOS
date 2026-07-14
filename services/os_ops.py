import psutil
import subprocess
import psutil
from services.platform import run_shell as _platform_run_shell,get_system_stats,run_python_module as _platform_run_python_module
import os
from services.file_system import _pick,_resolve_file,cd
from services.file_ops import _clean_name
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
def _path_to_module(path):
    path_lst=_resolve_file(path)
    path_of_choice=_pick(path_lst)
    if path_of_choice.endswith(".py"):
        path_of_choice=path_of_choice[:-3]
    path_of_choice = os.path.relpath(path_of_choice, PROJECT_ROOT)
    path_of_choice=path_of_choice.replace(os.sep,".")
    path_of_choice = path_of_choice.lstrip(".")
    return path_of_choice


def run_python_module(module_path,args=None,cwd=None):
    cwd=cd(cwd)
    if module_path.endswith(".py") or os.sep in module_path or "/" in module_path:
        module_path = _clean_name(module_path)
        print(module_path)
        module_path = _path_to_module(module_path)
    return _platform_run_python_module(module_path, args, cwd)
