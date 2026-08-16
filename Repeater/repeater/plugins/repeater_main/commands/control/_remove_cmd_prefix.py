from ...command_register import CommandCaller

def remove_cmd_prefix(command: str) -> str:
    command = command.strip()
    for delimiter in CommandCaller.delimiters():
        if command.startswith(delimiter):
            return command[len(delimiter):]

    raise ValueError(f"{command} not start with cmd_prefix")