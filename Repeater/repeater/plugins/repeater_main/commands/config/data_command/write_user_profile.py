from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class WriteUserProfile(BaseConfig):
    cmd = "writeUserProfile"
    aliases = {
        "wup",
        "WUP",
        "write_user_profile",
        "Write_User_Profile",
        "WriteUserProfile",
        "WRITE_USER_PROFILE",
    }
    field = "user_profile"
    description = f"""
    Customizing user portrait settings.

    Usage:
      /{cmd} user_portrait
    """

    # 字符串类型，不需要重写 parse_value
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: str
        ):
        await send_msg.send_response_check_code(response, f"User Profile set to {value}")