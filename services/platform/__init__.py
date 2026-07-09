import platform
system = platform.system()  # returns "Linux", "Windows", or "Darwin"

if system == "Windows":
    from services.platform.windows import run_shell, get_system_stats,run_python_module
elif system == "Darwin":
    from services.platform.mac import run_shell, get_system_stats,run_python_module
else:
    from services.platform.linux import run_shell, get_system_stats,run_python_module