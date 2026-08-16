from ....assist import PersonaInfo, SendMsg, Response, parse_delimited_string
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class SetStopKeywords(BaseConfig):
    cmd = "setStopKeywords"
    aliases = {
        "ssk",
        "SSK",
        "set_stop_keywords",
        "Set_Stop_Keywords",
        "SetStopKeywords",
        "SET_STOP_KEYWORDS",
    }
    field = "stop"

    async def parse_value(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
        raw_value: list[str] | None,
    )  -> list[str]:
        msg = persona_info.message_stripped_str
        value = parse_delimited_string(msg)
        if not value:
            await send_msg.send_error("Please enter at least one stop keyword.")
        return value
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: bool
        ):
        await send_msg.send_response_check_code(response, f"Set Stop Keywords to {', '.join(value)}")