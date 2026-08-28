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

    copyed_info = info.copy_with_args(
        info.make_message(
            pattern.sub(
                _fill_var,
                info.message_cqcode
            )
        )
    )
    return copyed_info