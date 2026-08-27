from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...clients import UserFileClient


@CommandCaller.register
class SendUserDataFile(CommandPackage):
    cmd = "sendUserDataFile"
    aliases = {
        "sudf",
        "SUDF",
        "send_user_data_file",
        "Send_User_Data_File",
        "SendUserDataFile",
        "SEND_USER_DATA_FILE",
    }
    cmd_type = CmdTypes.USERFILE
    description = f"""
    Export all the active data in user space.

    Usage:
    ```
    /{cmd}
    ```
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        user_configs = await persona_info.get_user_configs()
        user_file_client = UserFileClient(persona_info, user_configs)
        file_url = await user_file_client.get_user_data_file_url()
        await send_msg.send_file(file_url, f"{persona_info.namespace_str}_UserDataFile.zip")