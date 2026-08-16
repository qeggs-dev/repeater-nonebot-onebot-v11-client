from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class SetImageModelTimeout(BaseConfig):
    cmd = "setImageModelTimeout"
    aliases = {
        "simto",
        "SIMTO",
        "set_image_model_timeout",
        "Set_Image_Model_Timeout",
        "SetImageModelTimeout",
        "SET_IMAGE_MODEL_TIMEOUT",
    }
    field = "gen_image_timeout"

    async def parse_value(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
        raw_value: float | None,
    ) -> float:
        msg = persona_info.message_stripped_str
        try:
            value = int(msg)
        except ValueError:
            try:
                value = float(msg)
            except ValueError:
                await send_msg.send_error("Image Model Timeout setting is incorrect, please enter a number!")
        return value
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: float
        ):
        await send_msg.send_response_check_code(response, f"Set Image Model Timeout to {value}")