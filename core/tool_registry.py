

from services.file_system import (
    find_file,
    find_dir,
    read_file,
    get_ls,
    get_pwd,
    cd,
    _pick
)
from core.memory import (
    remember,
    get_all_history,
    clear_all_history
)
from core.analyser import (
    list_files,
    create_snapshot,
    summary
)
from services.fs_index import refresh_index
from services.file_ops import create_file, create_dir, move_file, move_dir, delete_dir, delete_file
from services.os_ops import get_system_usage, list_processes, kill_process, run_shell,run_python_module


def _resolve_maybe_list(result):
    return _pick(result) if isinstance(result, list) else result#same as _resolve_file and all


TOOL_REGISTRY = {
    ("filesystem", "find_file"): {
        "description": "Find a file by name. Returns its full path.",
        "schema": {
            "type": "function",
            "function": {
                "name": "filesystem_find_file",
                "description": "Find a file by name and return its full path.",
                "parameters": {
                    "type": "object",
                    "properties": {"name": {"type": "string"}},
                    "required": ["name"]
                }
            }
        },
        "fn": lambda args: _resolve_maybe_list(find_file(args.get("name")))
    },
    ("filesystem", "find_dir"): {
        "description": "Find a directory by name. Returns its full path.",
        "schema": {
            "type": "function",
            "function": {
                "name": "filesystem_find_dir",
                "description": "Find a directory by name and return its full path.",
                "parameters": {
                    "type": "object",
                    "properties": {"name": {"type": "string"}},
                    "required": ["name"]
                }
            }
        },
        "fn": lambda args: _resolve_maybe_list(find_dir(args.get("name")))
    },
    ("filesystem", "read_file"): {
        "description": "Read contents of a file at a known path.",
        "schema": {
            "type": "function",
            "function": {
                "name": "filesystem_read_file",
                "description": "Read the contents of a file.",
                "parameters": {
                    "type": "object",
                    "properties": {"path": {"type": "string"}},
                    "required": ["path"]
                }
            }
        },
        "fn": lambda args: read_file(args.get("path"))
    },
    ("filesystem", "list_dir"): {
        "description": "List contents INSIDE a known directory.",
        "schema": {
            "type": "function",
            "function": {
                "name": "filesystem_list_dir",
                "description": "List contents inside a known directory. Do not use to find/locate a directory.",
                "parameters": {
                    "type": "object",
                    "properties": {"path": {"type": "string"}},
                    "required": []
                }
            }
        },
        "fn": lambda args: get_ls(args.get("path", "."))
    },
    ("filesystem", "pwd"): {
        "description": "Show the current working directory.",
        "schema": {
            "type": "function",
            "function": {
                "name": "filesystem_pwd",
                "description": "Show the current working directory.",
                "parameters": {"type": "object", "properties": {}, "required": []}
            }
        },
        "fn": lambda args: get_pwd()
    },
    ("filesystem", "cd"): {
        "description": "Change the current working directory.",
        "schema": {
            "type": "function",
            "function": {
                "name": "filesystem_cd",
                "description": "Change the current working directory.",
                "parameters": {
                    "type": "object",
                    "properties": {"path": {"type": "string"}},
                    "required": ["path"]
                }
            }
        },
        "fn": lambda args: cd(args.get("path"))
    },
    ("memory", "remember"): {
        "description": "Store a fact in memory.",
        "schema": {
            "type": "function",
            "function": {
                "name": "memory_remember",
                "description": "Store a fact in memory. Only when the user wants to SAVE information.",
                "parameters": {
                    "type": "object",
                    "properties": {"fact": {"type": "string"}},
                    "required": ["fact"]
                }
            }
        },
        "fn": lambda args: remember({"fact": args.get("fact")})
    },
    ("memory", "clear"): {
        "description": "Clear all stored memory and history.",
        "schema": {
            "type": "function",
            "function": {
                "name": "memory_clear",
                "description": "Clear all stored memory and history.",
                "parameters": {"type": "object", "properties": {}, "required": []}
            }
        },
        "fn": lambda args: clear_all_history()
    },
    ("analyser", "project_summary"): {
        "description": "Analyse and summarize the entire project/repository.",
        "schema": {
            "type": "function",
            "function": {
                "name": "analyser_project_summary",
                "description": "Analyse and summarize the entire project/repository.",
                "parameters": {"type": "object", "properties": {}, "required": []}
            }
        },
        "fn": lambda args: summary(create_snapshot(list_files()))
    },
    ("filesystem", "refresh_index"): {
        "description": "Rebuild filesystem index (use after file changes)",
        "schema": {
            "type": "function",
            "function": {
                "name": "filesystem_refresh_index",
                "description": "Rebuild the filesystem index.",
                "parameters": {"type": "object", "properties": {}, "required": []}
            }
        },
        "fn": lambda args: refresh_index()
    },
    ("chat", "chat"): {
        "description": "Fallback for normal conversation.",
        "schema": None,
        "fn": lambda args: None
    },
    ("filesystem", "create_file"): {
        "description": "Create an empty file by name, optionally inside a folder.",
        "schema": {
            "type": "function",
            "function": {
                "name": "filesystem_create_file",
                "description": (
                "Create an empty file, optionally inside a folder. "
                "'dir' must be the BARE folder name only — never a phrase. "
                "Example: 'create chunk.json in core folder of controlled_lab' "
                "-> name='chunk.json', dir='core' (NOT 'core folder of controlled_lab', "
                "NOT 'core/folder of controlled_lab'). Ignore project/parent context "
                "words like 'of controlled_lab' — just take the single folder name "
                "right after 'in'/'inside'."
            ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "dir": {"type": "string", "description": "folder name to create it inside, if mentioned"}
                    },
                    "required": ["name"]
                }
            }
        },
        "fn": lambda args: create_file(args["name"], args.get("dir"))
    },
    ("filesystem", "create_dir"): {
        "description": "Create a directory by name, optionally inside a parent folder.",
        "schema": {
            "type": "function",
            "function": {
                "name": "filesystem_create_dir",
                "description": (
                "Create a directory, optionally inside a parent folder. "
                "'parent' must be the BARE folder name only — never a phrase. "
                "Example: 'create test folder in core folder of controlled_lab' "
                "-> name='test', parent='core' (NOT 'core folder of controlled_lab'). "
                "Ignore project/parent context words like 'of controlled_lab'."
            ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "parent": {"type": "string", "description": "parent folder name, if mentioned"}
                    },
                    "required": ["name"]
                }
            }
        },
        "fn": lambda args: create_dir(args["name"], args.get("parent"))
    },
    ("filesystem", "move_file"): {
        "description": "Move a file by name into a destination folder.",
        "schema": {
            "type": "function",
            "function": {
                "name": "filesystem_move_file",
                "description": "Move a file into a destination folder. This is one call, not two — ignore source-location mentions like 'from X'.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "dst_dir": {"type": "string"}
                    },
                    "required": ["name", "dst_dir"]
                }
            }
        },
        "fn": lambda args: move_file(args["name"], args.get("dst_dir"))
    },
    ("filesystem", "move_dir"): {
        "description": "Move a directory by name into a destination folder.",
        "schema": {
            "type": "function",
            "function": {
                "name": "filesystem_move_dir",
                "description": (
                "Move a directory into a destination folder. "
                "IMPORTANT: 'name' and 'dst_dir' must be BARE folder names only — "
                "strip filler words like 'folder', 'directory', 'the'. "
                "Example: 'move test folder from helixos to core folder of controlled_lab' "
                "-> name='test', dst_dir='core' (NOT 'test folder', NOT 'core/folder', "
                "NOT 'controlled_lab' — controlled_lab is just extra context, ignore it). "
                "This is one call, not two."
            ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "dst_dir": {"type": "string"}
                    },
                    "required": ["name", "dst_dir"]
                }
            }
        },
        "fn": lambda args: move_dir(args["name"], args.get("dst_dir"))
    },
    ("filesystem", "delete_file"): {
        "description": "Delete a file by name.",
        "schema": {
            "type": "function",
            "function": {
                "name": "filesystem_delete_file",
                "description": "Delete a file by name.",
                "parameters": {
                    "type": "object",
                    "properties": {"name": {"type": "string"}},
                    "required": ["name"]
                }
            }
        },
        "fn": lambda args: delete_file(args["name"])
    },
    ("filesystem", "delete_dir"): {
        "description": "Delete a directory and everything inside it.",
        "schema": {
            "type": "function",
            "function": {
                "name": "filesystem_delete_dir",
                "description": "Delete a directory and everything inside it.",
                "parameters": {
                    "type": "object",
                    "properties": {"name": {"type": "string"}},
                    "required": ["name"]
                }
            }
        },
        "fn": lambda args: delete_dir(args["name"])
    },
    ("os", "usage"): {
        "description": "Get current CPU, RAM and disk usage.",
        "schema": {
            "type": "function",
            "function": {
                "name": "os_usage",
                "description": "Get current CPU, RAM and disk usage.",
                "parameters": {"type": "object", "properties": {}, "required": []}
            }
        },
        "fn": lambda args: get_system_usage()
    },
    ("os", "list_processes"): {
        "description": "List running processes sorted by CPU usage.",
        "schema": {
            "type": "function",
            "function": {
                "name": "os_list_processes",
                "description": "List running processes sorted by CPU usage. Only for viewing, not stopping.",
                "parameters": {
                    "type": "object",
                    "properties": {"filter_name": {"type": "string"}},
                    "required": []
                }
            }
        },
        "fn": lambda args: list_processes(args.get("filter_name"))
    },
    ("os", "kill_process"): {
        "description": "Kill a process by name or pid.",
        "schema": {
            "type": "function",
            "function": {
                "name": "os_kill_process",
                "description": "Kill/stop/terminate a process by name or PID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "pid": {"type": "string"}
                    },
                    "required": []
                }
            }
        },
        "fn": lambda args: kill_process(args.get("name"), args.get("pid"))
    },
    ("os", "run_module"): {
    "description": "Run a Python module using python -m.",
    "schema": {
        "type": "function",
        "function": {
            "name": "os_run_module",
            "description": (
                "Run a Python file or module.\n"
                "\n"
                "Use this tool when the user says:\n"
                "- run a python file\n"
                "- execute a python file\n"
                "- launch a python file\n"
                "- python -m module\n"
                    "Execute Python code. "
    "Use this tool whenever the user says run, execute, start, launch, "
    "or test a .py file. "
    "NEVER use filesystem_find_file for execution requests. "
    "Examples: "
    "'run test.py' -> module_path='test.py' "
    "'execute tests/test_run.py' -> module_path='tests/test_run.py' "
                "\n"
                "IMPORTANT:\n"
                "Do NOT call find_file or find_dir before this tool.\n"
                "This tool automatically resolves files.\n"
                "\n"
                "Examples:\n"
                "run test_run.py in tests folder of Helixos\n"
                "module_path='tests/test_run.py'\n"
                "cwd='Helixos'\n"
                "\n"
                "run frontend terminal\n"
                "module_path='frontend.terminal'"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "module_path": {
                        "type": "string",
                        "description": (
                            "Python file or module to run. "
                            "Examples: test_run.py, tests/test_run.py, "
                            "frontend.terminal"
                        )
                    },
                    "args": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Optional command line arguments.",
                        "default": []
                    },
                    "cwd": {
                        "type": "string",
                        "description": (
                            "Project folder or working directory if mentioned "
                            "by the user."
                        )
                    }
                },
                "required": [
                    "module_path"
                ]
            }
        }
    },
    "fn": lambda args: run_python_module(
        module_path=args["module_path"],
        args=args.get("args", []),
        cwd=args.get("cwd")
    )
},
}


def get_tool_schemas():
    return [spec["schema"] for spec in TOOL_REGISTRY.values() if spec.get("schema") is not None]