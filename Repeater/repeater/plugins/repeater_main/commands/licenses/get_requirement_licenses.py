from nonebot.adapters.onebot.v11 import Message, MessageSegment
from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...clients import LicenseClient


@CommandCaller.register
class GetRequirementLicenses(CommandPackage):
    cmd = "getRequirementLicenses"
    aliases = {
        "grl",
        "GRL",
        "get_requirement_licenses",
        "Get_Requirement_Licenses",
        "GetRequirementLicenses",
        "GET_REQUIREMENT_LICENSES",
    }
    cmd_type = CmdTypes.LICENSES

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        user_configs = await persona_info.get_user_configs()
        license_client = LicenseClient(persona_info, user_configs)
        server_version = await license_client.get_requirement_license(persona_info.message_stripped_str)
        version_data = server_version.get_data()
        if version_data is None:
            await send_msg.send_error("Server license data is invalid.")
        else:
            message = Message()
            for name, license in version_data.items():
                message.append(MessageSegment.text(f"{name}:\n"))
                message.append(await send_msg.render_text(license, direct_output=True))
            await send_msg.send_prompt(message)