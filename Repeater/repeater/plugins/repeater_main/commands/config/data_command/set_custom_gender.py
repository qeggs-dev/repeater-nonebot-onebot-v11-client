from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class SetCustomGender(BaseConfig):
    cmd = "setCustomGender"
    aliases = {
        "scg",
        "SCG",
        "set_custom_gender",
        "Set_Custom_Gender",
        "SetCustomGender",
        "SET_CUSTOM_GENDER",
    }
    field = "user_gender"
    description = f"""
    Customize the setting of gender in a user profile.

    Usage:
      /{cmd} gender
    """
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: str
        ):
        await send_msg.send_response_check_code(response, f"Custom Gender set to {value}")