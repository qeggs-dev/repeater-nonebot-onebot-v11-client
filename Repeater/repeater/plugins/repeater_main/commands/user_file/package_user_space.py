from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...clients import UserFileClient


@CommandCaller.register
class PackageUserSpace(CommandPackage):
    cmd = "packageUserSpace"
    aliases = {
        "pus",
        "PUS",
        "package_user_space",
        "Package_User_Space",
        "PackageUserSpace",
        "PACKAGE_USER_SPACE",
    }
    cmd_type = CmdTypes.USERFILE
    description = f"""
    Export all the data in user space.

    Usage:
      /{cmd}
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        user_configs = await persona_info.get_user_configs()
        user_file_client = UserFileClient(persona_info, user_configs)
        file_url = await user_file_client.package_user_space_url()
        await send_msg.send_file(file_url, f"{persona_info.namespace_str}_PackageSpace.zip")