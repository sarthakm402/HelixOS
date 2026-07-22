from core.tool_registry import TOOL_REGISTRY, get_tool_schemas
from services.llm import get_tool_call_plan
from core.chat import ask


def build_plan(user_input):
    try:
        tool_calls = get_tool_call_plan(user_input, get_tool_schemas())
    except Exception as e:
        print(f"[helix warning] planner call failed, falling back to chat: {e}")
        return [{"tool": "chat", "action": "chat", "args": {}}]

    plan = []
    for call in tool_calls:
        fn_info = call.get("function", {})
        full_name = fn_info.get("name", "")
        args = fn_info.get("arguments", {}) or {}
        tool, _, action = full_name.partition("_")
        plan.append({"tool": tool, "action": action, "args": args})

    if not plan:
        plan = [{"tool": "chat", "action": "chat", "args": {}}]
    return plan


def execute_plan(plan, user_input):
    results = {}
    for step in plan:
        tool = step["tool"]
        action = step["action"]
        args = step.get("args", {})
        step_id = step.get("id")

        if tool == "chat":
            try:
                results[step_id or "chat"] = ask(user_input)
            except Exception as e:
                results[step_id or "chat"] = {"error": f"chat failed: {e}"}
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
    try:
        plan = build_plan(user_input)
    except Exception as e:
        return {"error": f"failed to build plan: {e}"}
    print(plan)
    try:
        return execute_plan(plan, user_input)
    except Exception as e:
        return {"error": f"failed to execute plan: {e}"}