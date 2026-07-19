import os
import sys
import subprocess
import psutil
from services.file_system import _pick, _resolve_file, _resolve_dir, cd
from services.platform import run_shell as _platform_run_shell, get_system_stats
from core import process_tracker


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
        targets = [{"pid": int(pid)}]
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
    return _platform_run_shell(command, timeout=timeout)


def _resolve_file_and_root(name, dir=None, cwd=None):
    resolved_file = _resolve_file(name, dir_hint=dir)
    if not resolved_file:
        return None, None, {"error": f"could not find file: {name}"}
    if isinstance(resolved_file, list):
        resolved_file = _pick(resolved_file)

    if cwd:
        resolved_root = _resolve_dir(cwd)
        if not resolved_root:
            return None, None, {"error": f"could not find project root: {cwd}"}
        if isinstance(resolved_root, list):
            resolved_root = _pick(resolved_root)
    else:
        resolved_root = os.path.dirname(resolved_file)

    return resolved_file, resolved_root, None


def run_python_module(name, dir=None, args=None, cwd=None):
    resolved_file, resolved_root, err = _resolve_file_and_root(name, dir, cwd)
    if err:
        return err

    env = os.environ.copy()
    env["PYTHONPATH"] = resolved_root + os.pathsep + env.get("PYTHONPATH", "")
    cmd = [sys.executable, resolved_file] + (args or [])

    process = subprocess.Popen(
        cmd, cwd=resolved_root, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )
    process_tracker.track(process.pid, "script", name, " ".join(cmd), resolved_root)

    stdout, _ = process.communicate()
    process_tracker.mark_finished(process.pid, process.returncode)

    return {"exit_code": process.returncode, "stdout": stdout, "pid": process.pid}


def start_server(name, dir=None, cwd=None, app_name="app", port=8000):
    resolved_file, resolved_root, err = _resolve_file_and_root(name, dir, cwd)
    if err:
        return err

    rel = os.path.relpath(resolved_file, resolved_root)
    if rel.endswith(".py"):
        rel = rel[:-3]
    dotted = rel.replace(os.sep, ".").lstrip(".")

    env = os.environ.copy()
    env["PYTHONPATH"] = resolved_root + os.pathsep + env.get("PYTHONPATH", "")
    cmd = [sys.executable, "-m", "uvicorn", f"{dotted}:{app_name}", "--reload", "--port", str(port)]

    process = subprocess.Popen(cmd, cwd=resolved_root, env=env)
    info = process_tracker.track(
        process.pid, "server", name, " ".join(cmd), resolved_root,
        extra={"port": port}
    )
    return {"status": "started", **info}


def list_helix_processes(kind=None):
    return process_tracker.list_processes(kind)
def stop_server(pid=None, name=None):
    target_pid = int(pid) if pid else None
    if not target_pid and name:
        for p in process_tracker.list_processes(kind="server"):
            if p["name"] == name and p["status"] == "running":
                target_pid = p["pid"]
                break
    if not target_pid:
        return {"error": "no matching running server found"}

    result = kill_process(pid=str(target_pid))
    process_tracker.mark_finished(target_pid, None)
    return result