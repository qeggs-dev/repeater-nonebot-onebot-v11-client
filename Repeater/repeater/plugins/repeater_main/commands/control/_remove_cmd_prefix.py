from ...command_register import CommandCaller

def remove_cmd_prefix(command: str) -> str:
    command = command.strip()
    cmd_prefixs = CommandCaller.cmd_prefixs()
    for delimiter in cmd_prefixs:
        if command.startswith(delimiter):
            return command.removeprefix(delimiter)

    if cmd_prefixs:
        raise ValueError(f"{command} not start with cmd_prefix")
    return command