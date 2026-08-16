from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class SetTemperature(BaseConfig):
    cmd = "setTemperature"
    aliases = {
        "st",
        "ST",
        "set_temperature",
        "Set_Temperature",
        "SetTemperature",
        "SET_TEMPERATURE",
    }
    field = "temperature"

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
            await send_msg.send_error("Temperature is set incorrectly. Please enter a floating-point number or percentage between 0 and 2!")
        if value < 0 or value > 2:
            await send_msg.send_error("Temperature is set incorrectly. Please enter a floating-point number or percentage between 0 and 2!")
        return value
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: float
        ):
        await send_msg.send_response_check_code(response, f"Set Temperature to {value}")