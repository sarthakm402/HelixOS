from services.llm import chat_with_llm
from core.memory import get_all_history,get_memories
def ask(user_query):
    history = get_all_history()
    conversation = "\n".join(
    f"{msg['role']}: {msg['content']}"
    for msg in history[-10:]
)
    memory_text = "\n".join(
    f"- {m['fact']}"
    for m in get_memories()
)
    prompt = f"""
Previous Conversation:

{conversation}
Memory:
{memory_text}
Current User Message:
{user_query}
"""
    for token in chat_with_llm(prompt):
        yield token
