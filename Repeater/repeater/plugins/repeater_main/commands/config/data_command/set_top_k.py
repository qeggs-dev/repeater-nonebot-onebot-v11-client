from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class SetTopK(BaseConfig):
    cmd = "setTopK"
    aliases = {
        "stk",
        "STK",
        "set_top_k",
        "Set_Top_K",
        "SetTopK",
        "SET_TOP_K",
    }
    field = "top_k"

    async def parse_value(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
        raw_value: int | None,
    )  -> int:
        msg = persona_info.message_stripped_str
        try:
            value = int(msg)
        except ValueError:
            await send_msg.send_error("Top_K setting error, please enter a positive integer or 0!")
        
        if value < 0:
            await send_msg.send_error("Top_K setting error, please enter a positive integer or 0!")
        return value
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: bool
        ):
        await send_msg.send_response_check_code(response, f"Set Top_K to {value}")