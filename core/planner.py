import json
from core.tool_registry import TOOL_REGISTRY
from core.chat import ask,complete_ans_of_llm
def get_tool_docs():
    docs = ""

    for (tool, action), spec in TOOL_REGISTRY.items():
        docs += f"""
Tool: {tool}
Action: {action}
Description: {spec['description']}

"""
    return docs
def build_planner_prompt(user_input):
    prompt = f"""
You are Helix Planner.

Your ONLY responsibility is to convert a user request into a JSON execution plan.

You are NOT:
- a chatbot
- a coding assistant
- a teacher
- a search engine

You MUST output ONLY valid JSON.

Never output:
- markdown
- explanations
- reasoning
- Python code
- comments
- text before JSON
- text after JSON

AVAILABLE TOOLS:

{get_tool_docs()}

VALID OUTPUT FORMAT:

[
  {{
    "tool": "tool_name",
    "action": "action_name",
    "args": {{}}
  }}
]

TOOL USAGE RULES

Use tools ONLY when the user wants to PERFORM an action.

Examples:

"find chat.py"
"read planner.py"
"change directory to core"
"remember my name is sarthak"
"clear memory"
"analyse this project"

These require tools.

--------------------------------

DO NOT use tools for normal questions.

Examples:

"what is my name"
"who am i"
"what do you remember about me"
"hello"
"how are you"
"summarize our conversation"
"what did i just say"

These MUST use:

[
  {{
    "tool":"chat",
    "action":"chat",
    "args": {{}}
  }}
]

--------------------------------

MEMORY RULES

Use memory.remember ONLY when the user wants to STORE information.

Examples:

"remember my name is sarthak"
"remember that i use ollama"

Use memory.clear ONLY when the user wants to DELETE memory.

Examples:

"clear memory"
"forget everything"

NEVER use memory tools to answer questions.

Questions about memories should always use:

[
  {{
    "tool":"chat",
    "action":"chat",
    "args": {{}}
  }}
]

--------------------------------

FILESYSTEM RULES

Use filesystem.find_file only when the user explicitly asks to find a file.

Good:

"find chat.py"

Bad:

"what is my name"

Never invent filenames.

Never assume files exist.

Never create filenames from user questions.

For example:

User:
"what is my name"

WRONG:

[
  {{
    "tool":"filesystem",
    "action":"find_file",
    "args": {{
      "name":"name.txt"
    }}
  }}
]

CORRECT:

[
  {{
    "tool":"chat",
    "action":"chat",
    "args": {{}}
  }}
]
--------------------------------

NESTED PATH RULE

When the user mentions one or more folders that contain a file or folder,
extract every folder mentioned, IN ORDER from outermost to innermost, as a
LIST in "path_hint". Do NOT join them into a single string yourself —
always output them as separate list items.

This applies no matter how many folders are mentioned: zero, one, two,
three, or more.

Examples:

"create chunk.json"
-> path_hint: []

"create notes.txt in logs"
-> path_hint: ["logs"]

"create chunk.json in core folder of helixos"
-> path_hint: ["helixos", "core"]

"create config.yaml in settings folder in src folder of backend"
-> path_hint: ["backend", "src", "settings"]

"put report.pdf inside archive, which is in reports, which is in 2024"
-> path_hint: ["2024", "reports", "archive"]

"delete notes.txt from logs folder in backend"
-> filesystem.delete_file args: {{"name": "notes.txt", "path_hint": ["backend", "logs"]}}

"move image.png to assets folder of frontend of website"
-> filesystem.move_file args: {{"name": "image.png", "path_hint": ["website", "frontend", "assets"]}}

Always list folders in the order a person would walk through them on disk —
outermost (the top-level folder) first, innermost (the folder that directly
contains the file) last. Never guess or invent folder names that were not
mentioned. Never collapse the list into a single joined string like
"helixos/core" — always a JSON list of separate strings.

--------------------------------
--------------------------------

FALLBACK RULE

If you are unsure, use:

[
  {{
    "tool":"chat",
    "action":"chat",
    "args": {{}}
  }}
]

--------------------------------

KILL PROCESS RULE

Use os.kill_process when the user wants to STOP or KILL a process.

Examples:

"kill stremio"      -> os.kill_process args: {{"name": "stremio"}}
"kill chrome"       -> os.kill_process args: {{"name": "chrome"}}
"terminate firefox" -> os.kill_process args: {{"name": "firefox"}}
"kill pid 1234"     -> os.kill_process args: {{"pid": "1234"}}

DO NOT use os.list_processes for kill requests.
os.list_processes is ONLY for when the user wants to SEE processes, not stop them.

USER REQUEST:

{user_input}
"""
    raw = complete_ans_of_llm(prompt)
    try:
        cleaned = (
        raw
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )
        plan = json.loads(cleaned)
        return plan
    except:
        print("did not work")
        return [
            {
                "tool":"chat",
                "action":"chat",
                "args":{}
            }
        ]
VALID_TOOLS = set(TOOL_REGISTRY.keys())

def validate_plan(plan):
    # not a list
    if not isinstance(plan, list):
        return False, "plan is not a list"
    
    # empty
    if len(plan) == 0:
        return False, "plan is empty"
    
    for step in plan:
        # missing keys
        if "tool" not in step:
            return False, f"step missing tool: {step}"
        if "action" not in step:
            return False, f"step missing action: {step}"
        
        # unknown tool
        if (step["tool"], step["action"]) not in VALID_TOOLS:
            return False, f"unknown tool: {step['tool']}.{step['action']}"
        
        # args must be a dict if present
        if "args" in step and not isinstance(step["args"], dict):
            return False, f"args must be a dict in step: {step}"
    
    return True, None
def execute_plan(plan, user_input):
    results = {}
    for step in plan:
        tool = step["tool"]
        action = step["action"]
        args = step.get("args", {})
        step_id = step.get("id")

        for k, v in args.items():
            if isinstance(v, str) and v.startswith("$"):
                ref = v[1:]
                args[k] = results.get(ref)

        if tool == "chat":
            results[step_id or "chat"] = ask(user_input)
            continue

        if (tool, action) not in TOOL_REGISTRY:
            results[step_id or f"{tool}.{action}"] = {
                "error": f"unknown tool: {tool}.{action}"
            }
            continue

        try:
            fn = TOOL_REGISTRY[(tool, action)]["fn"]
            result = fn(args)
        except KeyError as e:
            result = {"error": f"missing required arg: {str(e)}"}
        except Exception as e:
            result = {"error": f"{tool}.{action} failed: {str(e)}"}

        results[step_id or f"{tool}.{action}"] = result

    return list(results.values())[-1] if results else None
def run_agent(user_input):
    plan = build_planner_prompt(user_input)
    valid, reason = validate_plan(plan)
    if not valid:
        print(f"[planner] invalid plan — {reason}, falling back to chat")
        plan = [{"tool": "chat", "action": "chat", "args": {}}]
    
    return execute_plan(plan, user_input)