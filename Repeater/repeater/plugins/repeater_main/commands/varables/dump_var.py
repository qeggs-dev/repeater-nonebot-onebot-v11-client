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
class DumpVar(CommandPackage):
    cmd = "dumpVar"
    aliases = {
        "dv",
        "DV",
        "dump_var",
        "Dump_Var",
        "DumpVar",
        "DUMP_VAR",
    }
    cmd_type = CmdTypes.VARIABLE
    description = f"""
    Dump variables to user configs.

    Usage:
    ```
    /{cmd}
    ```
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        user_configs = await persona_info.get_user_configs()
        if user_configs.variables is None:
            user_configs.variables = Variables()

        if persona_info.namespace in CommandCaller.variables:
            variables = CommandCaller.variables[persona_info.namespace]
        else:
            await send_msg.send_error("No variables found.")

        variables.dump(user_configs, persona_info.message_stripped_str)
        await persona_info.set_user_configs(user_configs)