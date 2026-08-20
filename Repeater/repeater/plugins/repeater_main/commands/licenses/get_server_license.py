from nonebot.adapters.onebot.v11 import Message, MessageSegment
from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...clients import LicenseClient


@CommandCaller.register
class GetServerLicenses(CommandPackage):
    cmd = "getServerLicenses"
    aliases = {
        "gsl",
        "GSL",
        "get_server_licenses",
        "Get_Server_Licenses",
        "GetServerLicenses",
        "GET_SERVER_LICENSES",
    }
    description = f"""
    Get an open source license for the backend.

    Usage:
      /{cmd}
    """
    cmd_type = CmdTypes.LICENSES 

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        user_configs = await persona_info.get_user_configs()
        license_client = LicenseClient(persona_info, user_configs)
        server_version = await license_client.get_server_licenses()
        version_data = server_version.get_data()
        if version_data is None:
            await send_msg.send_error("Server License Data is Invalid.")
        else:
            message = Message()
            for name, license in version_data.items():
                message.append(MessageSegment.text(f"{name}:\n"))
                message.append(await send_msg.render_text(license, direct_output=True))
            await send_msg.send_prompt(message)