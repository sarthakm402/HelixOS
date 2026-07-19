import time
import psutil

_PROCESSES = {}  # pid -> info dict

def track(pid, kind, name, cmd, cwd, extra=None):
    info = {
        "pid": pid,
        "type": kind,          # "script" or "server"
        "name": name,
        "cmd": cmd,
        "cwd": cwd,
        "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "running",
    }
    if extra:
        info.update(extra)
    _PROCESSES[pid] = info
    return info

def mark_finished(pid, exit_code):
    if pid in _PROCESSES:
        _PROCESSES[pid]["status"] = "finished"
        _PROCESSES[pid]["exit_code"] = exit_code

def list_processes(kind=None):
    if kind:
        return [p for p in _PROCESSES.values() if p["type"] == kind]
    return list(_PROCESSES.values())