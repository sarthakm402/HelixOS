import json
from types import GeneratorType
from core.memory import add_message
from core.router import route_user_input
from services.fs_index import refresh_index

def init():
    print("Helix starting...")
    print("Building index...")
    refresh_index()
    print("Index built")
    print("Starting ollama...")
    try:
        import subprocess
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("[helix] ollama connected")
    except Exception:
        print("[helix] warning: ollama not reachable — start it with 'ollama serve'")

def format_result(result):
    if isinstance(result, dict) and "error" in result:
        msg = f"[helix error] {result['error']}"
        if "did_you_mean" in result:
            msg += f"\ndid you mean: {', '.join(result['did_you_mean'])}"
        return msg
    if isinstance(result, str):
        cleaned = result.replace("```json", "").replace("```", "").strip()
        try:
            parsed = json.loads(cleaned)
            return json.dumps(parsed, indent=2)
        except:
            return cleaned.replace("\\n", "\n").replace("\\t", "\t")
    if isinstance(result, dict) or isinstance(result, list):
        return json.dumps(result, indent=2)
    return str(result)

def main():
    print("================================== AI CYBERDECK v0.1 ==================================")
    init()
    while True:
        user_input = input("user> ")
        result = route_user_input(user_input)
        if result == "exit":
            break
        if result == "command executed":
            continue
        add_message({"role": "user", "content": user_input})
        print("Helix> ", end="")
        if isinstance(result, GeneratorType):
            assistant_response = ""
            for token in result:
                print(token, end="", flush=True)
                assistant_response += token
            print()
            add_message({"role": "assistant", "content": assistant_response})
        else:
            assistant_response = format_result(result)
            print(assistant_response)
            add_message({"role": "assistant", "content": assistant_response})

if __name__ == "__main__":
    main()