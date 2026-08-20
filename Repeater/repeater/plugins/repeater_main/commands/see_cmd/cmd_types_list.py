from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes

@CommandCaller.register
class CmdTypesList(CommandPackage):
    cmd = "cmdTypesList"
    aliases = {
        "ctl",
        "CTL",
        "cmd_types_list",
        "Cmd_Types_List",
        "CmdTypesList",
        "CMD_TYPES_LIST"
    }
    cmd_type = CmdTypes.SEE_CMD
    description = f"""
        List all command types.

        Usage:
        ```
        /{cmd}
        ```
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        total_count = len(CommandCaller.commands)
        text_buffer: list[str] = []
        text_buffer.append(f"Total: {total_count}")
        for cmd_type, types in CommandCaller.types.items():
            text_buffer.append(f"{cmd_type.value} ({len(types)}: {len(types) / total_count:.2%})")
        
        await send_msg.send_check_length_prompt(
            "\n".join(text_buffer)
        )
