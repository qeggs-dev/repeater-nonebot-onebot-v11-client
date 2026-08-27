from nonebot.config import Config
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...assist import PersonaInfo, SendMsg, parse_delimited_string
from ...cmd_info import CmdTypes
from ._assists import (
    all_splited_commands,
    see_cmds
)

@CommandCaller.register
class RegistedInfoTable(CommandPackage):
    cmd = "registedInfoTable"
    aliases = {
        "rit",
        "RIT",
        "registed_info_table",
        "Registed_Info_Table",
        "RegistedInfoTable",
        "REGISTED_INFO_TABLE"
    }
    cmd_type = CmdTypes.SEE_CMD
    description = f"""
        View the details of the registed commands.

        Usage:
        ```
        /{cmd}
        ```
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        tables = "\n".join(CommandCaller.registed_info_table())
        await send_msg.send_check_length_prompt(f"```\n{tables}\n```")
        