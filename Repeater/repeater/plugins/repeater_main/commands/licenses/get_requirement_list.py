from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...clients import LicenseClient


@CommandCaller.register
class GetRequirementList(CommandPackage):
    cmd = "getRequirementList"
    aliases = {
        "grls",
        "GRLS",
        "get_requirement_list",
        "Get_Requirement_List",
        "GetRequirementList",
        "GET_REQUIREMENT_LIST",
    }
    description = f"""
    Gets a list of requirements.

    Usage:
    ```
    /{cmd}
    ```
    """
    cmd_type = CmdTypes.LICENSES

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        user_configs = await persona_info.get_user_configs()
        license_client = LicenseClient(persona_info, user_configs)
        server_requirements = await license_client.get_requirement_list()
        version_data = server_requirements.get_data()
        if not version_data:
            await send_msg.send_error("Server requirements data is invalid.")
        else:
            text_buffer: list[str] = []
            for index, requirement in enumerate(version_data, start=1):
                text_buffer.append(f"{index}. {requirement}")
            await send_msg.send_check_length("\n".join(text_buffer))