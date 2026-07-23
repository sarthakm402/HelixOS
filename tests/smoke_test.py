"""
Helix Smoke Test

Purpose:
- Verify core tools don't crash after changes.
- Catch regressions in filesystem, process, Python runner, and server handling.
- Not a replacement for unit tests.

Prerequisites:
tests/
├── smoke_test.py
├── test_runner.py
└── test_api.py

test_runner.py:
----------------
print("HELIX_SMOKE_OK")

test_api.py:
------------
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

Run:
python tests/smoke_test.py
"""

import time
import requests

from services.file_system import (
    read_file,
    get_ls,
    find_file,
    find_dir,
    get_pwd,
)

from services.file_ops import (
    create_file,
    delete_file,
    create_dir,
    delete_dir,
)

from services.os_ops import (
    kill_process,
    list_processes,
    run_python_module,
    start_server,
    stop_server,
    list_helix_processes,
)

passed = 0
failed = 0


def check(label, condition):
    global passed, failed

    if condition:
        print(f"✅ PASS: {label}")
        passed += 1
    else:
        print(f"❌ FAIL: {label}")
        failed += 1


def safe_test(label, fn):
    try:
        result = fn()
        check(label, True)
        return result
    except Exception as e:
        print(f"Exception: {e}")
        check(label, False)
        return None


print("\n========== HELIX SMOKE TEST ==========\n")

# ==========================================================
# FILESYSTEM
# ==========================================================

print("--- Filesystem ---")

safe_test(
    "read missing file does not crash",
    lambda: read_file("this_file_should_not_exist.xyz"),
)

result = read_file("this_file_should_not_exist.xyz")

check(
    "missing file returns error",
    isinstance(result, dict) and "error" in result,
)

result = get_ls("this_directory_should_not_exist")

check(
    "missing directory returns error",
    isinstance(result, dict) and "error" in result,
)

safe_test(
    "find missing file does not crash",
    lambda: find_file("fake_file_xyz"),
)

safe_test(
    "find missing directory does not crash",
    lambda: find_dir("fake_directory_xyz"),
)

# ==========================================================
# FILE OPERATIONS
# ==========================================================

print("\n--- File Operations ---")

TEST_FILE = "helix_smoke_test.txt"

result = create_file(TEST_FILE)

check(
    "create_file works",
    isinstance(result, str)
    and "created" in result.lower(),
)

result = read_file(TEST_FILE)

check(
    "created file readable",
    isinstance(result, str),
)

result = delete_file(TEST_FILE)

check(
    "delete_file works",
    isinstance(result, str)
    and "deleted" in result.lower(),
)

# ==========================================================
# DIRECTORY OPERATIONS
# ==========================================================

TEST_DIR = "helix_smoke_directory"

result = create_dir(TEST_DIR)

check(
    "create_dir works",
    isinstance(result, str)
    and (
        "created" in result.lower()
        or "exists" in result.lower()
    ),
)

result = delete_dir(TEST_DIR)

check(
    "delete_dir works",
    isinstance(result, str)
    and (
        "deleted" in result.lower()
        or "removed" in result.lower()
    ),
)

# ==========================================================
# CURRENT DIRECTORY
# ==========================================================

print("\n--- Directory State ---")

result = get_pwd()

check(
    "pwd returns directory",
    isinstance(result, str)
    and len(result) > 0,
)

# ==========================================================
# PROCESS MANAGEMENT
# ==========================================================

print("\n--- Process Management ---")

result = list_processes()

check(
    "list_processes works",
    isinstance(result, list),
)

result = kill_process(
    name="this_process_should_not_exist_xyz123"
)

check(
    "kill nonexistent process handled",
    isinstance(result, dict)
    and "error" in result,
)

# ==========================================================
# HELIX PROCESS TRACKER
# ==========================================================

print("\n--- Process Tracker ---")

result = list_helix_processes()

check(
    "list_helix_processes works",
    isinstance(result, list),
)

# ==========================================================
# PYTHON RUNNER
# ==========================================================

print("\n--- Python Runner ---")

result = run_python_module(
    name="fake_script_xyz.py"
)

check(
    "missing python module handled",
    isinstance(result, dict)
    and "error" in result,
)

result = run_python_module(
    name="test_runner.py",
    dir="tests",
)

check(
    "runner returns dict",
    isinstance(result, dict),
)

check(
    "runner exit code == 0",
    result.get("exit_code") == 0,
)

check(
    "runner produced stdout",
    "HELIX_SMOKE_OK" in result.get("stdout", ""),
)

check(
    "runner returned pid",
    isinstance(result.get("pid"), int),
)

# ==========================================================
# SERVER LIFECYCLE
# ==========================================================

print("\n--- Server Lifecycle ---")

PORT = 8765

result = start_server(
    name="test_api.py",
    dir="tests",
    app_name="app",
    port=PORT,
)

check(
    "server started",
    isinstance(result, dict)
    and result.get("launch_status") == "started",
)

time.sleep(2)

try:
    response = requests.get(
        f"http://127.0.0.1:{PORT}/",
        timeout=5,
    )

    check(
        "server responds 200",
        response.status_code == 200,
    )

    check(
        "server returns expected json",
        response.json() == {"status": "ok"},
    )

except Exception as e:
    print(e)
    check("server reachable", False)

tracked = list_helix_processes(kind="server")

check(
    "server started",
    isinstance(result, dict)
    and "error" not in result
    and isinstance(result.get("pid"), int),
)

pid = None

for process in tracked:
    if process["name"] == "test_api.py" and process["status"] == "running":
        pid = process["pid"]
        break

check(
    "server pid located",
    pid is not None,
)

if pid is not None:
    result = stop_server(pid=pid)

    check(
        "stop_server succeeds",
        isinstance(result, str)
        or (
            isinstance(result, dict)
            and "error" not in result
        ),
    )

    time.sleep(1)

    try:
        requests.get(
            f"http://127.0.0.1:{PORT}/",
            timeout=2,
        )

        check(
            "server stopped",
            False,
        )

    except Exception:
        check(
            "server stopped",
            True,
        )

# ==========================================================
# SUMMARY
# ==========================================================

print("\n===================================")
print(f"PASSED : {passed}")
print(f"FAILED : {failed}")
print("===================================\n")

raise SystemExit(1 if failed else 0)