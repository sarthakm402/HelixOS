from services.file_system import (
    find_file,
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

TOOL_REGISTRY = {
    ("filesystem", "find_file"): {
        "description": "Find file or directory. args:{name,path}",
        "fn": lambda args: find_file(
            args.get("name"),
            args.get("path", ".")
        )
    },

    ("filesystem", "read_file"): {
        "description": "Read a file. args:{path}",
        "fn": lambda args: read_file(
            args.get("path")
        )
    },

    ("filesystem", "list_dir"): {
        "description": "List directory contents. args:{path}",
        "fn": lambda args: get_ls(
            args.get("path", ".")
        )
    },

    ("filesystem", "pwd"): {
        "description": "Current working directory",
        "fn": lambda args: get_pwd()
    },

    ("filesystem", "cd"): {
        "description": "Change directory. args:{path}",
        "fn": lambda args: cd(
            args.get("path")
        )
    },

    ("memory", "remember"): {
        "description": "Store memory. args:{fact}",
        "fn": lambda args: remember({
            "fact": args.get("fact")
        })
    },
    ("memory", "clear"): {
        "description": "Clear history",
        "fn": lambda args: clear_all_history()
    },

    ("analyser", "project_summary"): {
        "description": "Analyze repository",
        "fn": lambda args: summary(
            create_snapshot(
                list_files()
            )
        )
    }
}