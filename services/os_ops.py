import psutil
import subprocess
import psutil

def get_system_usage():
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.5),
        "ram_used_gb": round(psutil.virtual_memory().used / 1e9, 2),
        "ram_total_gb": round(psutil.virtual_memory().total / 1e9, 2),
        "ram_percent": psutil.virtual_memory().percent,
        "disk_used_gb": round(psutil.disk_usage("/").used / 1e9, 2),
        "disk_total_gb": round(psutil.disk_usage("/").total / 1e9, 2),
    }

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
    """Run a shell command safely. timeout in seconds."""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True,
            text=True, timeout=timeout
        )
        return {
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"error": f"timed out after {timeout}s"}