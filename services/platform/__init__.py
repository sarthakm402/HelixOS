import platform
system = platform.system()  # returns "Linux", "Windows", or "Darwin"

if system == "Windows":
    from services.platform.windows import run_shell, get_system_stats
elif system == "Darwin":
    from services.platform.mac import run_shell, get_system_stats
else:
    from services.platform.linux import run_shell, get_system_stats