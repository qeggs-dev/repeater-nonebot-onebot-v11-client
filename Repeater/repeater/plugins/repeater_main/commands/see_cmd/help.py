from ...command_register import(
    CommandCaller,
    CommandPackage
)
from nonebot.adapters.onebot.v11 import Message
from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...clients import VersionAPIClient
from ..._adaptation_info import __adaptation__
from .cmd_type import CmdType
from .cmd_types_list import CmdTypesList
from .see_cmd import SeeCmd
from .see_component import SeeComponent
from ..control.execute import Execute

@CommandCaller.register
class Help(CommandPackage):
    cmd = "help"
    aliases = {
        "h",
        "H",
        "Help",
        "HELP"
    }
    cmd_type = CmdTypes.SEE_CMD
    description = f"""
        View help information.

        Usage:
        ```
        /{cmd}
        ```
    """

    @staticmethod
    async def get_instance(package: type[CommandPackage], persona_info: PersonaInfo, send_msg: SendMsg) -> CommandPackage:
        try:
            package_instance = CommandCaller.get_instance(package)
        except KeyError:
            await send_msg.send_error(f"Get {package.__name__} instance failed.")
        return package_instance

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        message: Message = Message()
        text_buffer: list[str] = []

        user_configs = await persona_info.get_user_configs()
        version_api_client = VersionAPIClient(persona_info, user_configs)

        backend_version: str | None = None

        response = await version_api_client.get_version()
        if response:
            data = response.get_data()
            if data is not None:
                backend_version = data.core

        text_buffer.append("# Repeater LCSM")
        text_buffer.append("Repeater Series LLM Context State Management Middleware")
        text_buffer.append("OneBot V11 protocol adapter.")
        
        if backend_version is None:
            text_buffer.append("[Fetch backend version failed]")
        else:
            text_buffer.append(f"Version: {backend_version}")

        text_buffer.append(f"The scheduler version is {__adaptation__}")
        message.append("\n".join(text_buffer))
        text_buffer.clear()

        text_buffer.append("Enter any non-command content to talk to the AI.")
        text_buffer.append(f"Execute ")
        text_buffer.append(f"-  `{(await self.get_instance(CmdTypesList, persona_info, send_msg)).component}`(`/{CmdTypesList.cmd}`)")
        text_buffer.append("     to get all command types of the Repeater.")
        text_buffer.append(f"-  `{(await self.get_instance(CmdType, persona_info, send_msg)).component}`(`/{CmdType.cmd}`)")
        text_buffer.append("     to get information about all commands of the specified type.")
        text_buffer.append(f"-  `{(await self.get_instance(SeeCmd, persona_info, send_msg)).component}`(`/{SeeCmd.cmd}`)")
        text_buffer.append("     to view help information about a specific command.")
        text_buffer.append(f"-  `{(await self.get_instance(SeeComponent, persona_info, send_msg)).component}`(`/{SeeComponent.cmd}`)")
        text_buffer.append("     to view its information through component.")
        text_buffer.append(f"-  `{(await self.get_instance(Execute, persona_info, send_msg)).component}`(`/{Execute.cmd}`)")
        text_buffer.append("     to Execute commands from component.")
        message.append(await send_msg.render_text_to_msg_segment("\n".join(text_buffer)))

        message.append("Let's give it a try!")

        await send_msg.send_any(message)