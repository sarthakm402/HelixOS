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
from services.file_ops import create_file, create_dir, move_file, move_dir, delete_dir, delete_file
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
        "description": """Create an empty file by name. If the user mentions any
folders it should be created inside, extract them as a LIST in path_hint,
ordered OUTERMOST folder first, INNERMOST folder last. Do NOT join them into
a single string yourself. If no folder is mentioned, use an empty list.
Use when: 'create file X', 'make file X in Y', 'new file X in Y folder of Z'.
Examples:
  'create chunk.json'                                  -> {"name": "chunk.json", "path_hint": []}
  'create notes.txt in logs'                            -> {"name": "notes.txt", "path_hint": ["logs"]}
  'create chunk.json in core folder of helixos'          -> {"name": "chunk.json", "path_hint": ["helixos", "core"]}
  'create config.yaml in settings folder in src of backend' -> {"name": "config.yaml", "path_hint": ["backend", "src", "settings"]}
args: {name, path_hint?}""",
        "fn": lambda args: create_file(args["name"])
    },
    ("filesystem", "create_dir"): {
        "description": """Create a directory by name. If the user mentions any
parent folders it should be created inside, extract them as a LIST in
path_hint, ordered OUTERMOST first, INNERMOST last. Do NOT join them into a
single string yourself. If no parent is mentioned, use an empty list.
Use when: 'create folder X', 'make directory X', 'new folder X in Y'.
Examples:
  'create folder cache'                          -> {"name": "cache", "path_hint": []}
  'create folder cache in services'              -> {"name": "cache", "path_hint": ["services"]}
  'make dir logs inside src of backend'          -> {"name": "logs", "path_hint": ["backend", "src"]}
args: {name, path_hint?}""",
        "fn": lambda args: create_dir(args["name"])
    },
    ("filesystem", "move_file"): {
        "description": """Move a file by name into a destination folder.
Extract every folder mentioned for the DESTINATION as a LIST in path_hint,
ordered OUTERMOST first, INNERMOST last. Do NOT join them into a string.
Use when: 'move file X to Y', 'put X in Y'.
Examples:
  'move chunk.json to core'                           -> {"name": "chunk.json", "path_hint": ["core"]}
  'move chunk.json to core folder of helixos'         -> {"name": "chunk.json", "path_hint": ["helixos", "core"]}
args: {name, path_hint}""",
        "fn": lambda args: move_file(args["name"])
    },
    ("filesystem", "move_dir"): {
        "description": """Move a directory by name into a destination folder.
Extract every folder mentioned for the DESTINATION as a LIST in path_hint,
ordered OUTERMOST first, INNERMOST last. Do NOT join them into a string.
Use when: 'move folder X to Y', 'move directory X into Y'.
Examples:
  'move folder cache to backend'                      -> {"name": "cache", "path_hint": ["backend"]}
  'move folder cache to src folder of backend'        -> {"name": "cache", "path_hint": ["backend", "src"]}
args: {name, path_hint}""",
        "fn": lambda args: move_dir(args["name"])
    },
    ("filesystem", "delete_file"): {
        "description": """Delete a file by name. If the user mentions any
folders the file is inside, extract them as a LIST in path_hint, ordered
OUTERMOST first, INNERMOST last, to disambiguate between files with the
same name in different folders. If no folder is mentioned, use an empty list.
Use when: 'delete file X', 'remove file X', 'delete X from Y folder of Z'.
Examples:
  'delete notes.txt'                                    -> {"name": "notes.txt", "path_hint": []}
  'delete notes.txt from logs folder in backend'        -> {"name": "notes.txt", "path_hint": ["backend", "logs"]}
args: {name, path_hint?}""",
        "fn": lambda args: delete_file(args["name"])
    },
    ("filesystem", "delete_dir"): {
        "description": """Delete a directory and everything inside it. If the
user mentions any parent folders, extract them as a LIST in path_hint,
ordered OUTERMOST first, INNERMOST last, to disambiguate folders with the
same name in different locations. If no parent is mentioned, use an empty list.
Use when: 'delete folder X', 'remove directory X'.
Examples:
  'delete folder cache'                                 -> {"name": "cache", "path_hint": []}
  'delete folder cache inside backend'                  -> {"name": "cache", "path_hint": ["backend"]}
args: {name, path_hint?}""",
        "fn": lambda args: delete_dir(args["name"])
    },

    ("os", "usage"): {
        "description": """Get current CPU, RAM and disk usage.
Use when: 'system usage', 'cpu usage', 'how much ram am i using', 'disk space', 'system stats'.
No args.""",
        "fn": lambda args: get_system_usage()
    },
    ("os", "list_processes"): {
        "description": """List running processes sorted by CPU usage.
Use when: 'list processes', 'what is running', 'show processes', 'ps', 'top processes', 'running apps'.
args: {filter_name?} optional, filter by process name""",
        "fn": lambda args: list_processes(args.get("filter_name"))
    },
    ("os", "kill_process"): {
        "description": """Kill a process by name or pid.
Use when: 'kill X', 'terminate X', 'stop process X', 'kill pid 1234'.
Prefer name over pid when user gives a name.
args: {name?, pid?}""",
        "fn": lambda args: kill_process(args.get("name"), args.get("pid"))
    },
}