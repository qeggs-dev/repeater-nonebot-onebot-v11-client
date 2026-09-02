import re
from ...assist import PersonaInfo, Variables

pattern = re.compile(r"\{\s*var\s*:\s*([\w\.]+)\s*\}")

def fill_var(info: PersonaInfo, vars: Variables) -> PersonaInfo:
    """
    Fill variables with the given values.
    """

    def _fill_var(match_group: re.Match[str]) -> str:
        nonlocal vars
        var_name = match_group.group(1)
        return vars.get(var_name, "")

    messages: list[str] = info.message_cqcode.splitlines()
    new_messages: list[str] = []
    for line in messages:
        if not line.startswith(" "):
            new_line = pattern.sub(_fill_var, line)
            new_messages.append(new_line)
        else:
            new_messages.append(line)

    copyed_info = info.copy(
        args = info.make_message(
            message = "\n".join(new_messages)
        )
    )
    return copyed_info