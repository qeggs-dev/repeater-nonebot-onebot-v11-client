from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class SetCustomAge(BaseConfig):
    cmd = "setCustomAge"
    aliases = {
        "sca",
        "SCA",
        "set_custom_age",
        "Set_Custom_Age",
        "SetCustomAge",
        "SET_CUSTOM_AGE",
    }
    field = "user_age"
    description = f"""
    Customize the age setting in a user profile.

    Usage:
      /{cmd} age
    """

    async def parse_value(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
        raw_value: int | float | None,
    )  -> int | float:
        msg = persona_info.message_stripped_str
        try:
            value = int(msg)
        except ValueError:
            try:
                value = float(msg)
            except ValueError:
                await send_msg.send_error("Please input a number.")
        return value
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: int
        ):
        await send_msg.send_response_check_code(response, f"Custom Age set to {value}")