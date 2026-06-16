import json
from core.tool_registry import TOOL_REGISTRY
from core.chat import ask,complete_ans_of_llm
def get_tool_docs():
    docs = ""
    for (tool, action), spec in TOOL_REGISTRY.items():
        docs += f"{tool}.{action} : {spec['description']}\n"
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
def execute_plan(plan, user_input):
    result = None
    for step in plan:
        tool = step["tool"]
        action = step["action"]
        if tool == "chat":
            result = ask(user_input)
            continue
        if (tool, action) not in TOOL_REGISTRY:
            continue
        fn = TOOL_REGISTRY[
            (tool, action)
        ]["fn"]
        result = fn(
            step.get("args", {})
        )
    return result
def run_agent(user_input):
    plan = build_planner_prompt(user_input)
    print("PLAN:")
    print(plan)
    return execute_plan(
        plan,
        user_input
    )