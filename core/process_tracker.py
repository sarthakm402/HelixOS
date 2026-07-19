import time
import json
import os
import psutil

TRACKER_FILE = os.path.expanduser("~/.helix_processes.json")


def _load():
    if os.path.exists(TRACKER_FILE):
        try:
            with open(TRACKER_FILE) as f:
                return {int(k): v for k, v in json.load(f).items()}
        except (json.JSONDecodeError, ValueError):
            return {}
    return {}


def _save():
    with open(TRACKER_FILE, "w") as f:
        json.dump(_PROCESSES, f, indent=2)


_PROCESSES = _load()


def track(pid, kind, name, cmd, cwd, extra=None):
    info = {
        "pid": pid,
        "type": kind,
        "name": name,
        "cmd": cmd,
        "cwd": cwd,
        "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "running",
    }
    if extra:
        info.update(extra)
    _PROCESSES[pid] = info
    _save()
    return info


def mark_finished(pid, exit_code):
    if pid in _PROCESSES:
        _PROCESSES[pid]["status"] = "finished"
        _PROCESSES[pid]["exit_code"] = exit_code
        _save()


def list_processes(kind=None):
    # for pid, info in list(_PROCESSES.items()):
    #     if info["status"] == "running" and not psutil.pid_exists(pid):
    #         info["status"] = "stopped"
    _save()
    if kind:
        return [p for p in _PROCESSES.values() if p["type"] == kind]
    return list(_PROCESSES.values())