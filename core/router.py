from core.chat import ask
from core.handle_system_commands import handle_commands
def route_user_input(user_input):
    if user_input.startswith("/"):
        return handle_commands(user_input)
    return ask(user_input)