from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class SetTopA(BaseConfig):
    cmd = "setTopA"
    aliases = {
        "sta",
        "STA",
        "set_top_a",
        "Set_Top_A",
        "SetTopA",
        "SET_TOP_A",
    }
    field = "top_a"

    async def parse_value(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
        raw_value: float | None,
    )  -> float:
        msg = persona_info.message_stripped_str
        try:
            value = float(msg)
        except ValueError:
            await send_msg.send_error("Top_A setting error, please enter a positive number or 0!")
        
        if value < 0:
            await send_msg.send_error("Top_A setting error, please enter a positive number or 0!")
        return value
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: bool
        ):
        await send_msg.send_response_check_code(response, f"Set Top_A to {value}")