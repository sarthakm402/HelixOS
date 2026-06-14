# from core.chat import ask
# from core.handle_system_commands import handle_commands
# def route_user_input(user_input):
#     if user_input.startswith("/"):
#         return handle_commands(user_input)
#     return ask(user_input)
from core.handle_system_commands import (
    handle_commands
)
from core.planner import run_agent
def route_user_input(user_input):
    if user_input.startswith("/"):
        return handle_commands(user_input)
    return run_agent(user_input)