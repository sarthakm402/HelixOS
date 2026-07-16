import subprocess
import psutil
import time
import subprocess
import shutil
from services.file_system import cd

import os
import sys
import subprocess

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

def run_python_module(script_path, args=None, cwd=None):
    env = os.environ.copy()
    if cwd:
        # Prepend the project root to PYTHONPATH so the child process can resolve
# project-local imports (e.g., `core.memory`) regardless of its launch location,
# while preserving any existing PYTHONPATH entries.
      env["PYTHONPATH"] = cwd + os.pathsep + env.get("PYTHONPATH", "")

    process = subprocess.Popen(
        [sys.executable, script_path] + (args or []),
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    stdout, _ = process.communicate()
    return {
        "exit_code": process.returncode,
        "stdout": stdout,
    }