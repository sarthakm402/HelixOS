from services.llm import chat_with_llm
from core.memory import get_all_history
def ask(user_query):
    history = get_all_history()
    conversation = "\n".join(
    f"{msg['role']}: {msg['content']}"
    for msg in history[-10:]
)
    prompt = f"""
Previous Conversation:

{conversation}

Current User Message:
{user_query}
"""
    for token in chat_with_llm(prompt):
        yield token
