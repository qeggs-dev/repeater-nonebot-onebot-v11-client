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
        total_count: int = 0
        cmd_types: list[tuple[CmdTypes, int]] = []
        for cmd_type, types in CommandCaller.types.items():
            cmd_types.append((cmd_type, len(types)))
            total_count += len(types)

        cmd_types.sort(key=lambda x: x[1], reverse=True)

        text_buffer: list[str] = [
            f"Total: {total_count}",
            "Command Types:"
        ]
        for index, (cmd_type, count) in enumerate(cmd_types, start=1):
            text_buffer.append(f"{index}. Repeater.{cmd_type.value}: {count}({count / total_count:.2%})")
        
        await send_msg.send_check_length_prompt(
            "\n".join(text_buffer)
        )
