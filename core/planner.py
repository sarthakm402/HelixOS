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
        if not isinstance(args, dict):
            args = {}
        tool, _, action = full_name.partition("_")
        plan.append({"tool": tool, "action": action, "args": args})

    if not plan:
        plan = [{"tool": "chat", "action": "chat", "args": {}}]
    return plan


def _resolve_step_refs(args, results):
    """Replace any '$stepId' string values with the actual result from that step."""
    resolved = {}
    for k, v in args.items():
        if isinstance(v, str) and v.startswith("$"):
            ref_id = v[1:]
            resolved[k] = results.get(ref_id, v)  # fall back to literal if not found
        else:
            resolved[k] = v
    return resolved


def execute_plan(plan, user_input):
    results = {}
    last_result = None

    for i, step in enumerate(plan):
        tool = step.get("tool", "")
        action = step.get("action", "")
        args = step.get("args", {}) or {}
        step_id = step.get("id") or f"__step{i}"

        if tool == "chat":
            try:
                last_result = ask(user_input)
            except Exception as e:
                last_result = {"error": f"chat failed: {e}"}
            results[step_id] = last_result
            continue

        if (tool, action) not in TOOL_REGISTRY:
            last_result = {"error": f"unknown tool: {tool}.{action}"}
            results[step_id] = last_result
            continue

        try:
            resolved_args = _resolve_step_refs(args, results)
            fn = TOOL_REGISTRY[(tool, action)]["fn"]
            result = fn(resolved_args)
        except KeyError as e:
            result = {"error": f"missing required arg: {str(e)}"}
        except Exception as e:
            result = {"error": f"{tool}.{action} failed: {str(e)}"}

        results[step_id] = result
        last_result = result

    return last_result


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