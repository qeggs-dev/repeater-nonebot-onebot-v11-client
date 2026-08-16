from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class SetRepetitionPenalty(BaseConfig):
    cmd = "setRepetitionPenalty"
    aliases = {
        "srp",
        "SRP",
        "set_repetition_penalty",
        "Set_Repetition_Penalty",
        "SetRepetitionPenalty",
        "SET_REPETITION_PENALTY",
    }
    field = "repetition_penalty"

    async def parse_value(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
        raw_value: float | None,
    )  -> float | None:
        msg = persona_info.message_stripped_str
        try:
            if msg.endswith("%"):
                msg = msg[:-1]
                value = float(msg) / 100
            else:
                value = float(msg)
        except ValueError:
            await send_msg.send_error("Repetition_Penalty setting is incorrect, please enter a floating-point number or percentage between 0 and 2!")
        
        if value == 0:
            return None

        if value <= 0 or value > 2:
            await send_msg.send_error("Repetition_Penalty setting is incorrect, please enter a floating-point number or percentage between 0 and 2!")
        return value
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: float | None,
        ):
        if value is None:
            await send_msg.send_response_check_code(response, f"Set Repetition_Penalty to default")
        else:
            await send_msg.send_response_check_code(response, f"Set Repetition_Penalty to {value}")