# from services.file_system import (
#     find_file,
#     find_dir,
#     read_file,
#     get_ls,
#     get_pwd,
#     cd,
#     _pick
# )
# from core.memory import (
#     remember,
#     get_all_history,
#     clear_all_history
# )
# from core.analyser import (
#     list_files,
#     create_snapshot,
#     summary
# )
# from services.fs_index import refresh_index
# from services.file_ops import create_file, create_dir, move_file, move_dir, delete_dir, delete_file
# from services.os_ops import get_system_usage, list_processes, kill_process, run_shell


# def _resolve_maybe_list(result):
#     return _pick(result) if isinstance(result, list) else result


# TOOL_REGISTRY = {
#     ("filesystem", "find_file"): {
#         "description": """Find a file by name. Returns its full path.
# Use when: 'find chat.py', 'where is planner.py', 'locate main.py'
# args: {name}""",
#         "fn": lambda args: _resolve_maybe_list(find_file(args.get("name")))
#     },
#     ("filesystem", "find_dir"): {
#         "description": """Find a directory by name. Returns its full path.
# Use when: 'find folder services', 'where is core directory', 'locate envs folder'
# args: {name}""",
#         "fn": lambda args: _resolve_maybe_list(find_dir(args.get("name")))
#     },
#     ("filesystem", "read_file"): {
#         "description": """Read contents of a file at a known path.
# Use when user says: 'read X', 'show contents of X', 'open X', 'what is in X'.
# Examples:
#   'read planner.py'        -> filesystem.read_file args: {"path": "planner.py"}
#   'show contents of main'  -> filesystem.read_file args: {"path": "main.py"}
# args: {path}""",
#         "fn": lambda args: read_file(args.get("path"))
#     },
#     ("filesystem", "list_dir"): {
#         "description": """List contents INSIDE a known directory.
# Use ONLY when user says: 'list files in X', 'show contents of X folder', 'ls X', 'what is inside X'.
# Examples:
#   'list files in core'     -> filesystem.list_dir args: {"path": "core"}
#   'ls services'            -> filesystem.list_dir args: {"path": "services"}
#   'what is inside core'    -> filesystem.list_dir args: {"path": "core"}
# DO NOT use this to find or locate a directory.
# args: {path}""",
#         "fn": lambda args: get_ls(args.get("path", "."))
#     },
#     ("filesystem", "pwd"): {
#         "description": """Show the current working directory.
# Use ONLY when user says: 'where am I', 'current directory', 'pwd', 'what directory am I in'.
# Examples:
#   'where am I'             -> filesystem.pwd args: {}
#   'what is current dir'    -> filesystem.pwd args: {}
# DO NOT use this to find or locate files or folders.
# No args.""",
#         "fn": lambda args: get_pwd()
#     },
#     ("filesystem", "cd"): {
#         "description": """Change the current working directory.
# Use when user says: 'go to X', 'change directory to X', 'cd X', 'navigate to X'.
# Examples:
#   'cd core'                -> filesystem.cd args: {"path": "core"}
#   'go to services'         -> filesystem.cd args: {"path": "services"}
#   'navigate to ..'         -> filesystem.cd args: {"path": ".."}
# args: {path}""",
#         "fn": lambda args: cd(args.get("path"))
#     },
#     ("memory", "remember"): {
#         "description": """Store a fact in memory.
# Use ONLY when user wants to SAVE information: 'remember X', 'save that X', 'note that X'.
# Examples:
#   'remember my name is sarthak' -> memory.remember args: {"fact": "user name is sarthak"}
#   'remember I use ollama'        -> memory.remember args: {"fact": "user uses ollama"}
# DO NOT use this to answer questions about memory.
# args: {fact}""",
#         "fn": lambda args: remember({"fact": args.get("fact")})
#     },
#     ("memory", "clear"): {
#         "description": """Clear all stored memory and history.
# Use ONLY when user says: 'clear memory', 'forget everything', 'reset memory', 'wipe memory'.
# Examples:
#   'clear memory'           -> memory.clear args: {}
#   'forget everything'      -> memory.clear args: {}
# No args.""",
#         "fn": lambda args: clear_all_history()
#     },
#     ("analyser", "project_summary"): {
#         "description": """Analyse and summarize the entire project/repository.
# Use when user says: 'analyse project', 'summarize codebase', 'what does this project do', 'project overview'.
# Examples:
#   'analyse this project'   -> analyser.project_summary args: {}
#   'summarize the codebase' -> analyser.project_summary args: {}
# No args.""",
#         "fn": lambda args: summary(create_snapshot(list_files()))
#     },
#     ("filesystem", "refresh_index"): {
#         "description": "Rebuild filesystem index (use after file changes)",
#         "fn": lambda args: refresh_index()
#     },
#     ("chat", "chat"): {
#         "description": """Fallback for normal conversation, questions, and anything that does not require a tool.
# Use when user asks questions, greets, or chats.
# Examples:
#   'what is my name'        -> chat.chat args: {}
#   'hello'                  -> chat.chat args: {}
#   'what do you remember'   -> chat.chat args: {}
# No args.""",
#         "fn": lambda args: None  # handled separately in execute_plan
#     },

#     ("filesystem", "create_file"): {
#         "description": """Create an empty file by name, optionally inside a folder.
# If the user mentions a folder to create it in, extract just that folder NAME as dir
# (a single string, not a list). If no folder is mentioned, omit dir.
# Use when: 'create file X', 'make file X in Y', 'new file X in Y folder'.
# Examples:
#   'create chunk.json'                       -> {"name": "chunk.json"}
#   'create notes.txt in logs'                -> {"name": "notes.txt", "dir": "logs"}
#   'create chunk.json in core folder'        -> {"name": "chunk.json", "dir": "core"}
# args: {name, dir?}""",
#         "fn": lambda args: create_file(args["name"], args.get("dir"))
#     },
#     ("filesystem", "create_dir"): {
#         "description": """Create a directory by name, optionally inside a parent folder.
# If the user mentions a parent folder, extract just that folder NAME as parent
# (a single string, not a list). If no parent is mentioned, omit parent.
# Use when: 'create folder X', 'make directory X', 'new folder X in Y'.
# Examples:
#   'create folder cache'               -> {"name": "cache"}
#   'create folder cache in services'   -> {"name": "cache", "parent": "services"}
# args: {name, parent?}""",
#         "fn": lambda args: create_dir(args["name"], args.get("parent"))
#     },
#     ("filesystem", "move_file"): {
#         "description": """Move a file by name into a destination folder.
# Extract the destination folder NAME as dst_dir (a single string, not a list).
# Use when: 'move file X to Y', 'put X in Y'.
# Examples:
#   'move chunk.json to core'   -> {"name": "chunk.json", "dst_dir": "core"}
# args: {name, dst_dir}""",
#         "fn": lambda args: move_file(args["name"], args.get("dst_dir"))
#     },
#     ("filesystem", "move_dir"): {
#         "description": """Move a directory by name into a destination folder.
# Extract the destination folder NAME as dst_dir (a single string, not a list).
# Use when: 'move folder X to Y', 'move directory X into Y'.
# Examples:
#   'move folder cache to backend'   -> {"name": "cache", "dst_dir": "backend"}
# args: {name, dst_dir}""",
#         "fn": lambda args: move_dir(args["name"], args.get("dst_dir"))
#     },
#     ("filesystem", "delete_file"): {
#         "description": """Delete a file by name.
# Use when: 'delete file X', 'remove file X'.
# Examples:
#   'delete notes.txt'   -> {"name": "notes.txt"}
# args: {name}""",
#         "fn": lambda args: delete_file(args["name"])
#     },
#     ("filesystem", "delete_dir"): {
#         "description": """Delete a directory and everything inside it.
# Use when: 'delete folder X', 'remove directory X'.
# Examples:
#   'delete folder cache'   -> {"name": "cache"}
# args: {name}""",
#         "fn": lambda args: delete_dir(args["name"])
#     },

#     ("os", "usage"): {
#         "description": """Get current CPU, RAM and disk usage.
# Use when: 'system usage', 'cpu usage', 'how much ram am i using', 'disk space', 'system stats'.
# No args.""",
#         "fn": lambda args: get_system_usage()
#     },
#     ("os", "list_processes"): {
#         "description": """List running processes sorted by CPU usage.
# Use when: 'list processes', 'what is running', 'show processes', 'ps', 'top processes', 'running apps'.
# args: {filter_name?} optional, filter by process name""",
#         "fn": lambda args: list_processes(args.get("filter_name"))
#     },
#     ("os", "kill_process"): {
#         "description": """Kill a process by name or pid.
# Use when: 'kill X', 'terminate X', 'stop process X', 'kill pid 1234'.
# Prefer name over pid when user gives a name.
# args: {name?, pid?}""",
#         "fn": lambda args: kill_process(args.get("name"), args.get("pid"))
#     },
# }

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
    "description": "Run a Python module using `python -m`.",
    "schema": {
        "type": "function",
        "function": {
            "name": "os_run_module",
            "description": (
              " Runs `python -m <module_path> [args...]` in a new terminal window. "
    "module_path can be a dotted path (`frontend.terminal`) OR a bare filename/relative "
    "path (`test_run.py`, `tests/test_run.py`) — resolution happens automatically inside "
    "this tool. cwd should be the project root (e.g. the folder named by the user, like "
    "'helixos' -> its root path) so the file/module is found and resolved correctly. "
    "ALWAYS call this tool directly for requests like 'run X.py in <project>' or "
    "'run X.py from <project>' — do NOT call a separate file-search tool first. "
    "Just pass module_path exactly as the user said (filename or dotted path) and cwd "
    "as the project root; this tool handles finding and resolving the file internally."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "module_path": {
                        "type": "string",
                        "description": (
                            "Python module in dotted notation, e.g. "
                            "`frontend.terminal` or `tests.test_run`."
                        ),
                    },
                    "args": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional command-line arguments.",
                        "default": [],
                    },
                    "cwd": {
                        "type": "string",
                        "description": (
                            "Working directory (typically the project root) from "
                            "which to execute the module."
                        ),
                    },
                },
                "required": ["module_path"],
            },
        },
    },
    "fn": lambda args: run_python_module(
        module_path=args["module_path"],
        args=args.get("args", []),
        cwd=args.get("cwd"),
    ),
},
}


def get_tool_schemas():
    return [spec["schema"] for spec in TOOL_REGISTRY.values() if spec.get("schema") is not None]