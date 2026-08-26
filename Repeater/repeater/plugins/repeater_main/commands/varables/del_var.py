import re
from ...assist import (
    PersonaInfo,
    SendMsg,
    Variables
)
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...cmd_info import CmdTypes

@CommandCaller.register
class RemoveVar(CommandPackage):
    cmd = "RmvVar"
    aliases = {
        "rv",
        "RV",
        "remove_var",
        "Remove_Var",
        "RemoveVar",
        "REMOVE_VAR",
    }
    cmd_type = CmdTypes.VARIABLE
    description = f"""
    Remove a variable.

    Usagge:
      /{cmd} <var_name>
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        var_name = persona_info.message_stripped_str
        variables = CommandCaller.variables.get(persona_info.namespace)
        
        if variables is None:
            await send_msg("No variables found.")
            return

        if var_name not in variables:
            await send_msg(f"Variable \"{var_name}\" not found.")
            return

        del variables[var_name]
        await send_msg(f"Variable \"{var_name}\" removed.")