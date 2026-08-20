from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class SetTopP(BaseConfig):
    cmd = "setTopP"
    aliases = {
        "stp",
        "STP",
        "set_top_p",
        "Set_Top_P",
        "SetTopP",
        "SET_TOP_P",
    }
    field = "top_p"
    description = f"""
    Set Top_P

    Usage:
      /{cmd} top_p
    """

    async def parse_value(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
        raw_value: float | None,
    )  -> float:
        msg = persona_info.message_stripped_str
        try:
            if msg.endswith("%"):
                msg = msg[:-1]
                value = float(msg) / 100
            else:
                value = float(msg)
        except ValueError:
            await send_msg.send_error("Top_P setting error, please enter a floating-point number or percentage between 0 and 1!")
        if value < 0 or value > 1:
            await send_msg.send_error("Top_P setting error, please enter a floating-point number or percentage between 0 and 1!")
        return value
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: float,
        ):
        await send_msg.send_response_check_code(response, f"Set Top_P to {value}")