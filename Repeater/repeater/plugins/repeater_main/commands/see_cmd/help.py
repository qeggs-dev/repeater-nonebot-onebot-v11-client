from ...command_register import(
    CommandCaller,
    CommandPackage
)
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
    documents = f"""
        View help information.

        Usage:
        ```
        /{cmd}
        ```
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        text_buffer: list[str] = []

        user_configs = await persona_info.get_user_configs()
        version_api_client = VersionAPIClient(persona_info, user_configs)

        backend_version: str | None = None

        response = await version_api_client.get_version()
        if response:
            data = response.get_data()
            if data is not None:
                backend_version = data.core

        if backend_version is None:
            text_buffer.append("# Repeater [Fetch Backend Version Failed]")
        
        else:
            text_buffer.append(f"# Repeater {backend_version}")

        text_buffer.append(f"The scheduler version is {__adaptation__}")
        text_buffer.append("")

        text_buffer.append("Enter any non-command content to talk to the AI.")
        text_buffer.append(f"Execute \"{CmdTypesList.component}\" to get all command types of the Repeater.")
        text_buffer.append(f"Execute \"{CmdType.component}\" to get information about all commands of the specified type.")
        text_buffer.append(f"Execute \"{SeeCmd.component}\" to view help information about a specific command.")
        text_buffer.append(f"Execute \"{SeeComponent.component}\" to view its information through component.")
        text_buffer.append(f"Use {Execute.component} to Execute commands from component.")
        text_buffer.append("")

        text_buffer.append("Let's give it a try!")

        await send_msg.send_text("\n".join(text_buffer))