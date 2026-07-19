

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
from services.os_ops import get_system_usage, list_processes, kill_process, run_shell, run_python_module
from services.os_ops import get_system_usage, list_processes, kill_process, run_shell, run_python_module, start_server, list_helix_processes,stop_server

def _resolve_maybe_list(result):
    return _pick(result) if isinstance(result, list) else result


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
        "description": "Read contents of a file, optionally scoped to a folder.",
        "schema": {
            "type": "function",
            "function": {
                "name": "filesystem_read_file",
                "description": (
                    "Read the contents of a file. "
                    "'path' is the bare filename, e.g. 'config.json'. "
                    "'dir' is the folder it's inside, if mentioned, as a bare folder name — "
                    "used only to disambiguate duplicate filenames."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "dir": {"type": "string"}
                    },
                    "required": ["path"]
                }
            }
        },
        "fn": lambda args: read_file(args.get("path"), dir=args.get("dir"))
    },

    ("filesystem", "list_dir"): {
        "description": "List contents inside a known directory.",
        "schema": {
            "type": "function",
            "function": {
                "name": "filesystem_list_dir",
                "description": (
                    "List contents inside a directory. "
                    "'path' is the bare folder name, e.g. 'tests'. "
                    "'dir' is an optional parent-folder hint to disambiguate duplicate names. "
                    "Do not use to find/locate a directory — use filesystem_find_dir for that."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "dir": {"type": "string"}
                    },
                    "required": []
                }
            }
        },
        "fn": lambda args: get_ls(args.get("path", "."), dir=args.get("dir"))
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
                "description": (
                    "Change the current working directory. "
                    "'path' is the bare folder name, e.g. 'tests'. "
                    "'dir' is an optional parent-folder hint to disambiguate duplicate names."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "dir": {"type": "string"}
                    },
                    "required": ["path"]
                }
            }
        },
        "fn": lambda args: cd(args.get("path"), dir=args.get("dir"))
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
                    "-> name='chunk.json', dir='core' (NOT 'core folder of controlled_lab'). "
                    "Ignore project/parent context words like 'of controlled_lab' — just take "
                    "the single folder name right after 'in'/'inside'."
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
                "description": (
                    "Move a file into a destination folder. "
                    "'name' is the bare filename. 'dst_dir' is the bare destination folder name. "
                    "'src_dir' is an optional source-folder hint to disambiguate duplicate filenames — "
                    "ignore source-location phrases like 'from X' unless needed for disambiguation. "
                    "This is one call, not two."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "dst_dir": {"type": "string"},
                        "src_dir": {"type": "string"}
                    },
                    "required": ["name", "dst_dir"]
                }
            }
        },
        "fn": lambda args: move_file(args["name"], args.get("dst_dir"), src_dir=args.get("src_dir"))
    },

    ("filesystem", "move_dir"): {
        "description": "Move a directory by name into a destination folder.",
        "schema": {
            "type": "function",
            "function": {
                "name": "filesystem_move_dir",
                "description": (
                    "Move a directory into a destination folder. "
                    "'name' and 'dst_dir' must be BARE folder names only — strip filler words like "
                    "'folder', 'directory', 'the'. "
                    "Example: 'move test folder from helixos to core folder of controlled_lab' "
                    "-> name='test', dst_dir='core', src_dir='helixos' "
                    "(NOT 'test folder', NOT 'core/folder', NOT 'controlled_lab' — that's just context). "
                    "This is one call, not two."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "dst_dir": {"type": "string"},
                        "src_dir": {"type": "string"}
                    },
                    "required": ["name", "dst_dir"]
                }
            }
        },
        "fn": lambda args: move_dir(args["name"], args.get("dst_dir"), src_dir=args.get("src_dir"))
    },

    ("filesystem", "delete_file"): {
        "description": "Delete a file by name.",
        "schema": {
            "type": "function",
            "function": {
                "name": "filesystem_delete_file",
                "description": (
                    "Delete a file by name. "
                    "'dir' is an optional folder hint to disambiguate duplicate filenames."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "dir": {"type": "string"}
                    },
                    "required": ["name"]
                }
            }
        },
        "fn": lambda args: delete_file(args["name"], dir=args.get("dir"))
    },

    ("filesystem", "delete_dir"): {
        "description": "Delete a directory and everything inside it.",
        "schema": {
            "type": "function",
            "function": {
                "name": "filesystem_delete_dir",
                "description": (
                    "Delete a directory and everything inside it. "
                    "'dir' is an optional parent-folder hint to disambiguate duplicate names."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "dir": {"type": "string"}
                    },
                    "required": ["name"]
                }
            }
        },
        "fn": lambda args: delete_dir(args["name"], dir=args.get("dir"))
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
        "description": "Run a Python file.",
        "schema": {
            "type": "function",
            "function": {
                "name": "os_run_module",
                "description": (
                    "Run/execute/launch/test a Python file. "
                    "'name' must be the BARE filename only, e.g. 'test_run.py' "
                    "(never a path like 'tests/test_run.py' or 'tests.test_run.py'). "
                    "'dir' is the folder the file is inside, if mentioned, as a bare folder "
                    "name, used to disambiguate if multiple files share a name, e.g. 'tests'. "
                    "'cwd' is the PROJECT ROOT folder to run it from, if mentioned, as a bare "
                    "folder/project name, e.g. 'Helixos' or 'controlled_lab'. "
                    "Examples: "
                    "'run test_run.py in tests folder of Helixos' -> name='test_run.py', dir='tests', cwd='Helixos' "
                    "'execute logs/test_run.py in controlled_lab' -> name='test_run.py', dir='logs', cwd='controlled_lab' "
                    "'run test.py' -> name='test.py'"
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "dir": {"type": "string"},
                        "cwd": {"type": "string"},
                        "args": {
                            "type": "array",
                            "items": {"type": "string"},
                            "default": []
                        }
                    },
                    "required": ["name"]
                }
            }
        },
        "fn": lambda args: run_python_module(
            name=args["name"],
            dir=args.get("dir"),
            args=args.get("args", []),
            cwd=args.get("cwd")
        )
    },
    ("os", "start_server"): {
        "description": "Start a FastAPI/uvicorn server.",
        "schema": {
            "type": "function",
            "function": {
                "name": "os_start_server",
                "description": (
                    "Start a FastAPI app via uvicorn. Use for 'run as server', 'start the API', "
                    "'run fastapi', 'serve X'. 'name' is the bare filename, 'dir'/'cwd' as usual "
                    "(bare folder names, not phrases). 'app_name' is the FastAPI variable name "
                    "in the file, default 'app'. 'port' defaults to 8000 unless mentioned."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "dir": {"type": "string"},
                        "cwd": {"type": "string"},
                        "app_name": {"type": "string", "default": "app"},
                        "port": {"type": "integer", "default": 8000}
                    },
                    "required": ["name"]
                }
            }
        },
        "fn": lambda args: start_server(
            name=args["name"], dir=args.get("dir"), cwd=args.get("cwd"),
            app_name=args.get("app_name", "app"), port=args.get("port", 8000)
        )
    },

    ("os", "list_helix_processes"): {
        "description": "List scripts/servers Helix has run.",
        "schema": {
            "type": "function",
            "function": {
                "name": "os_list_helix_processes",
                "description": (
                    "List processes Helix has launched — scripts and servers, running or finished. "
                    "Optionally filter with 'kind': 'script' or 'server'. "
                    "Use when user asks 'what's running', 'is my server up', 'show my processes'."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "kind": {"type": "string", "enum": ["script", "server"]}
                    },
                    "required": []
                }
            }
        },
        "fn": lambda args: list_helix_processes(args.get("kind"))
    },
    ("os", "stop_server"): {
    "description": "Stop a running server by name or pid.",
    "schema": {
        "type": "function",
        "function": {
            "name": "os_stop_server",
            "description": (
                "Stop a server previously started with os_start_server, by name or pid. "
                "Use for 'stop the server', 'kill test_run server', 'shut down uvicorn'."
            ),
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
    "fn": lambda args: stop_server(pid=args.get("pid"), name=args.get("name"))
},

}


def get_tool_schemas():
    return [spec["schema"] for spec in TOOL_REGISTRY.values() if spec.get("schema") is not None]