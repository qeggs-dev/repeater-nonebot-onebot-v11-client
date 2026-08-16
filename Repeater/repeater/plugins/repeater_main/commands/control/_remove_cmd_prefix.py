from ...command_register import CommandCaller

def remove_cmd_prefix(command: str) -> str:
    for delimiter in CommandCaller.delimiters():
        if command.startswith(delimiter):
            return command[len(delimiter):]

    raise ValueError("Invalid command format")