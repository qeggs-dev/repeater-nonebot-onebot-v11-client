from ....assist import PersonaInfo, SendMsg, Response, str_to_bool
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class CrossUserDataAccess(BaseConfig):
    cmd = "crossUserDataAccess"
    aliases = {
        "cuda",
        "CUDA",
        "cross_user_data_access",
        "Cross_User_Data_Access",
        "CrossUserDataAccess",
        "CROSS_USER_DATA_ACCESS"
    }
    field = "cross_user_data_access"
    documents = f"""
    Set whether to allow cross user data access

    Usage:
      /{cmd} true
      /{cmd} false
    """

    async def parse_value(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
        raw_value: bool | None,
    )  -> bool:
        try:
            value = str_to_bool(persona_info.message_stripped_str)
        except ValueError:
            await send_msg.send_error("Not a valid boolean value")
        return value
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: bool
        ):
        await send_msg.send_response_check_code(response, f"Set Cross User Data Access to {value}")