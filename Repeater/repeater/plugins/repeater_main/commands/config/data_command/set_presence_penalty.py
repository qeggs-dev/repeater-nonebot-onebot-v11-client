from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class SetPresencePenalty(BaseConfig):
    cmd = "setPresencePenalty"
    aliases = {
        "spp",
        "SPP",
        "set_presence_penalty",
        "Set_Presence_Penalty",
        "SetPresencePenalty",
        "SET_PRESENCE_PENALTY",
    }
    field = "presence_penalty"
    description = f"""
    Set Presence Penalty

    Usage:
      /{cmd} presence_penalty
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
            await send_msg.send_error("Presence_Penalty is set incorrectly. Please enter a floating-point number or percentage between -2 and 2!")
        if value < -2 or value > 2:
            await send_msg.send_error("Presence_Penalty is set incorrectly. Please enter a floating-point number or percentage between -2 and 2!")
        return value
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: float,
        ):
        await send_msg.send_response_check_code(response, f"Set Presence_Penalty to {value}")