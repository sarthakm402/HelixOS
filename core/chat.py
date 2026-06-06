from services.llm import chat_with_llm
def ask(prompt):
    for token in chat_with_llm(prompt):
        yield token