from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class SetTimezone(BaseConfig):
    cmd = "setTimezone"
    aliases = {
        "stz",
        "STZ",
        "set_timezone",
        "Set_Timezone",
        "SetTimezone",
        "SET_TIMEZONE",
    }
    field = "timezone"
    description = f"""
    Set User's Timezone

    Usage:
      /{cmd} timezone
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
        await send_msg.send_response_check_code(response, f"Set Timezone to {value}")