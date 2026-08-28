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
class SeeComponent(CommandPackage):
    cmd = "seeComponent"
    aliases = {
        "scmp",
        "scmp",
        "see_component",
        "See_Component",
        "SeeComponent",
        "SEE_COMPONENT"
    }
    cmd_type = CmdTypes.SEE_CMD
    description = f"""
        View the details of the specified command.

        Usage:
        ```
        /{cmd} components
        ```
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        commands: dict[CmdTypes, list[CommandPackage]] = {}

        cmd_component: str = persona_info.message_stripped_str
        try:
            package: type[CommandPackage] = CommandCaller.match_component(cmd_component)
        except KeyError: 
            await send_msg.send_error(f"\"{cmd_component}\" is Not A Valid Command.")
            return

        try:
            package_instance: CommandPackage = CommandCaller.get_instance(package)
        except KeyError:
            await send_msg.send_error(f"Get \"{cmd_component}\" instance failed.")
            return

        commands[package.cmd_type] = [package_instance]

        delimiters = CommandCaller.delimiters()
        
        await see_cmds(
            delimiters = delimiters,
            commands = commands,
            persona_info = persona_info,
            send_msg = send_msg
        )