from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class SetMaxTokens(BaseConfig):
    cmd = "setMaxTokens"
    aliases = {
        "smt",
        "SMT",
        "set_max_tokens",
        "Set_Max_Tokens",
        "SetMaxTokens",
        "SET_MAX_TOKENS",
    }
    field = "max_tokens"
    description = f"""
    Set the maximum generated Token length for the model.
    If it is too small, truncation may occur,
    preallocation can waste some end space if it is too large, causing the model context cap to appear early.

    Usage:
      /{cmd} max_tokens
    """

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
            await send_msg.send_error("Max_Tokens setting is incorrect, please enter an integer!")
        if value < 1 or value > 8192:
            await send_msg.send_error("Max_Tokens setting is incorrect, please enter an integer between 1 and 8192!")
        return value
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: int
        ):
        await send_msg.send_response_check_code(response, f"Set Max_Tokens to {value}")