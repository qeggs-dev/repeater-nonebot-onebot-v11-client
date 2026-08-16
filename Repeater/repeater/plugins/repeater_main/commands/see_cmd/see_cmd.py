from nonebot.config import Config
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ._assists import (
    all_splited_commands,
    see_cmds
)

@CommandCaller.register
class SeeCmd(CommandPackage):
    cmd = "seeCmd"
    aliases = {
        "sc",
        "sc",
        "see_cmd",
        "See_Cmd",
        "SeeCmd",
        "SEE_CMD"
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
        commands: dict[CmdTypes, list[CommandPackage]] = {}

        cmd_name: str = persona_info.message_stripped_str
        delimiters = CommandCaller.delimiters()
        cmd_names: set[str | tuple[str, ...]] = set()

        if cmd_name:
            matched_times: int = 0
            for delimiter in delimiters:
                if delimiter in cmd_name:
                    matched_times += 1
                    for splited in all_splited_commands(cmd_name, delimiters):
                        cmd_names.add(splited)
            if matched_times == 0:
                cmd_names.add(cmd_name)
        
        for name in cmd_names:
            if name in CommandCaller.triggers:
                package = CommandCaller.triggers[name]
                package_instance = CommandCaller.commands[package]
                commands.setdefault(package.cmd_type, []).append(package_instance)
        
        if not commands:
            await send_msg.send_error(f"\"{cmd_name}\" is Not A Valid Command")
        
        await see_cmds(
            delimiters = delimiters,
            commands = commands,
            send_msg = send_msg
        )