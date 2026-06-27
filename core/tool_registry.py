from services.file_system import (
    find_file,
    find_dir,
    read_file,
    get_ls,
    get_pwd,
    cd
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
from services.file_ops import create_file, create_dir, move_file, move_dir,delete_dir,delete_file
from services.os_ops import get_system_usage, list_processes, kill_process, run_shell

TOOL_REGISTRY = {
    ("filesystem", "find_file"): {
    "description": """Find a file by name. Returns its full path.
Use when: 'find chat.py', 'where is planner.py', 'locate main.py'
args: {name}""",
    "fn": lambda args: find_file(args.get("name"))
},
    ("filesystem", "find_dir"): {
    "description": """Find a directory by name. Returns its full path.
Use when: 'find folder services', 'where is core directory', 'locate envs folder'
args: {name}""",
    "fn": lambda args: find_dir(args.get("name"))
},
    ("filesystem", "read_file"): {
        "description": """Read contents of a file at a known path.
Use when user says: 'read X', 'show contents of X', 'open X', 'what is in X'.
Examples:
  'read planner.py'        -> filesystem.read_file args: {"path": "planner.py"}
  'show contents of main'  -> filesystem.read_file args: {"path": "main.py"}
args: {path}""",
        "fn": lambda args: read_file(
            args.get("path")
        )
    },
    ("filesystem", "list_dir"): {
        "description": """List contents INSIDE a known directory.
Use ONLY when user says: 'list files in X', 'show contents of X folder', 'ls X', 'what is inside X'.
Examples:
  'list files in core'     -> filesystem.list_dir args: {"path": "core"}
  'ls services'            -> filesystem.list_dir args: {"path": "services"}
  'what is inside core'    -> filesystem.list_dir args: {"path": "core"}
DO NOT use this to find or locate a directory.
args: {path}""",
        "fn": lambda args: get_ls(
            args.get("path", ".")
        )
    },
    ("filesystem", "pwd"): {
        "description": """Show the current working directory.
Use ONLY when user says: 'where am I', 'current directory', 'pwd', 'what directory am I in'.
Examples:
  'where am I'             -> filesystem.pwd args: {}
  'what is current dir'    -> filesystem.pwd args: {}
DO NOT use this to find or locate files or folders.
No args.""",
        "fn": lambda args: get_pwd()
    },
    ("filesystem", "cd"): {
        "description": """Change the current working directory.
Use when user says: 'go to X', 'change directory to X', 'cd X', 'navigate to X'.
Examples:
  'cd core'                -> filesystem.cd args: {"path": "core"}
  'go to services'         -> filesystem.cd args: {"path": "services"}
  'navigate to ..'         -> filesystem.cd args: {"path": ".."}
args: {path}""",
        "fn": lambda args: cd(
            args.get("path")
        )
    },
    ("memory", "remember"): {
        "description": """Store a fact in memory.
Use ONLY when user wants to SAVE information: 'remember X', 'save that X', 'note that X'.
Examples:
  'remember my name is sarthak' -> memory.remember args: {"fact": "user name is sarthak"}
  'remember I use ollama'        -> memory.remember args: {"fact": "user uses ollama"}
DO NOT use this to answer questions about memory.
args: {fact}""",
        "fn": lambda args: remember({
            "fact": args.get("fact")
        })
    },
    ("memory", "clear"): {
        "description": """Clear all stored memory and history.
Use ONLY when user says: 'clear memory', 'forget everything', 'reset memory', 'wipe memory'.
Examples:
  'clear memory'           -> memory.clear args: {}
  'forget everything'      -> memory.clear args: {}
No args.""",
        "fn": lambda args: clear_all_history()
    },
    ("analyser", "project_summary"): {
        "description": """Analyse and summarize the entire project/repository.
Use when user says: 'analyse project', 'summarize codebase', 'what does this project do', 'project overview'.
Examples:
  'analyse this project'   -> analyser.project_summary args: {}
  'summarize the codebase' -> analyser.project_summary args: {}
No args.""",
        "fn": lambda args: summary(
            create_snapshot(
                list_files()
            )
        )
    },
    ("filesystem", "refresh_index"): {
    "description": "Rebuild filesystem index (use after file changes)",
    "fn": lambda args: refresh_index()
},
    ("chat", "chat"): {
        "description": """Fallback for normal conversation, questions, and anything that does not require a tool.
Use when user asks questions, greets, or chats.
Examples:
  'what is my name'        -> chat.chat args: {}
  'hello'                  -> chat.chat args: {}
  'what do you remember'   -> chat.chat args: {}
No args.""",
        "fn": lambda args: None  # handled separately in execute_plan
    },
    
("filesystem", "create_file"): {
    "description": """Create an empty file by name, optionally inside a directory.
Use when: 'create file X', 'make file X in Y', 'new file X in Y'.
args: {name, dir?}""",
    "fn": lambda args: create_file(args["name"], args.get("dir"))
},
("filesystem", "create_dir"): {
    "description": """Create a directory by name, optionally inside another directory.
Use when: 'create folder X', 'make directory X', 'new folder X in Y'.
args: {name, parent?}""",
    "fn": lambda args: create_dir(args["name"], args.get("parent"))
},
("filesystem", "move_file"): {
    "description": """Move a file by name into a destination directory.
Use when: 'move file X to Y', 'put X in Y'.
args: {name, dst_dir}""",
    "fn": lambda args: move_file(args["name"], args["dst_dir"])
},
("filesystem", "move_dir"): {
    "description": """Move a directory by name into another directory.
Use when: 'move folder X to Y', 'move directory X into Y'.
args: {name, dst_dir}""",
    "fn": lambda args: move_dir(args["name"], args["dst_dir"])
},
 ("filesystem", "delete_file"): {
    "description": """Delete a file by name.
Use when: 'delete file X', 'remove file X'.
args: {name}""",
    "fn": lambda args: delete_file(args["name"])
},
("filesystem", "delete_dir"): {
    "description": """Delete a directory and everything inside it.
Use when: 'delete folder X', 'remove directory X'.
args: {name}""",
    "fn": lambda args: delete_dir(args["name"])
},

}
