from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ._assists import see_cmds
from typing import Type

@CommandCaller.register
class CmdType(CommandPackage):
    cmd = "cmdType"
    aliases = {
        "ct",
        "ct",
        "cmd_type",
        "Cmd_Type",
        "CmdType",
        "CMD_TYPE"
    }
    cmd_type = CmdTypes.SEE_CMD
    documents = f"""
        View the details of the specified command.

        Usage:
        ```
        /{cmd} command
        ```
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        commands: list[CommandPackage] = []

        try:
            cmd_type = CmdTypes(persona_info.message_striped_str)
        except ValueError:
            await send_msg.send_error("Invalid command type.")
            return

        if cmd_type not in CommandCaller.types:
            await send_msg.send_error(f"\"{cmd_type}\" is not a valid command type.")
            return
        now_type_cmds: list[Type[CommandPackage]] = CommandCaller.types[cmd_type]
        commands = [CommandCaller.commands[cmd] for cmd in now_type_cmds]
        
        if not now_type_cmds:
            await send_msg.send_error(f"\"{cmd_type}\" has not any commands")

        text_buffer: list[str] = []
        for cmd in commands:
            text_buffer.append(cmd.component)

        await send_msg.send_check_length_prompt(
            "\n".join(text_buffer)
        )