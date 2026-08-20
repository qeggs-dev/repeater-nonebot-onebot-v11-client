from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...clients import VersionAPIClient
from ..._adaptation_info import __adaptation__


@CommandCaller.register
class AdaptationInfo(CommandPackage):
    cmd = "adaptationInfo"
    aliases = {
        "adai",
        "ADAI",
        "adaptation_info",
        "Adaptation_Info",
        "AdaptationInfo",
        "ADAPTATION_INFO",
    }
    cmd_type = CmdTypes.VERSION
    description = f"""
    Get the adaptation information.

    Usage:
      /{cmd}
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        user_configs = await persona_info.get_user_configs()
        version_client = VersionAPIClient(persona_info, user_configs)
        server_version = await version_client.get_version()
        version_data = server_version.get_data()
        if version_data is None:
            await send_msg.send_error("Server Version Data is Invalid")
            return
        await send_msg.send_prompt(
            (
                f"Client Adaptation Version: {__adaptation__}\n"
                f"Server Core Version: {version_data.core}"
            )
        )