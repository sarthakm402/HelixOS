import subprocess
import psutil

def run_shell(command, timeout=10):
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

import psutil

def get_system_stats():
    disk = psutil.disk_usage("/")
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    cpu = psutil.cpu_percent(interval=1)

    return {
        "cpu": {
            "usage_percent": cpu,
            "cores_logical": psutil.cpu_count(),
            "cores_physical": psutil.cpu_count(logical=False),
        },
        "memory": {
            "used_gb": round(memory.used / 1e9, 2),
            "available_gb": round(memory.available / 1e9, 2),
            "total_gb": round(memory.total / 1e9, 2),
            "percent": memory.percent,
        },
        "swap": {
            "used_gb": round(swap.used / 1e9, 2),
            "total_gb": round(swap.total / 1e9, 2),
            "percent": swap.percent,
        },
        "disk": {
            "used_gb": round(disk.used / 1e9, 2),
            "free_gb": round(disk.free / 1e9, 2),
            "total_gb": round(disk.total / 1e9, 2),
            "percent": disk.percent,
        }
    }