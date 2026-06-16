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

YOUR ONLY JOB:
Convert the user request into a JSON execution plan.

You are NOT:
- a coding assistant
- a chatbot
- a teacher
- an explainer

You MUST NEVER:
- write Python code
- write examples
- explain your reasoning
- use markdown
- use ```json
- use ```tool_code
- output any text before or after the JSON

AVAILABLE TOOLS:

{get_tool_docs()}

VALID SCHEMA:

[
  {{
    "tool": "tool_name",
    "action": "action_name",
    "args": {{}}
  }}
]

RULES:

1. Every tool MUST exist in the available tools list.
2. Every action MUST exist in the available tools list.
3. Never invent tools.
4. Never invent actions.
5. If no tool is appropriate, return:

[
  {{
    "tool": "chat",
    "action": "chat",
    "args": {{}}
  }}
]

EXAMPLES

User:
find chat.py

Output:
[
  {{
    "tool": "filesystem",
    "action": "find_file",
    "args": {{
      "name": "chat.py"
    }}
  }}
]

User:
remember that I use Ollama

Output:
[
  {{
    "tool": "memory",
    "action": "remember",
    "args": {{
      "fact": "I use Ollama"
    }}
  }}
]

User:
hello

Output:
[
  {{
    "tool": "chat",
    "action": "chat",
    "args": {{}}
  }}
]

IMPORTANT:

Your response will be parsed using json.loads().

If you output ANYTHING except valid JSON,
the system will fail.

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