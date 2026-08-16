from ....assist import PersonaInfo, SendMsg, Response, parse_delimited_string
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class SetMultipleModel(BaseConfig):
    cmd = "setMultipleModel"
    aliases = {
        "smm",
        "SMM",
        "set_multiple_model",
        "Set_Multiple_Model",
        "SetMultipleModel",
        "SET_MULTIPLE_MODEL",
    }
    field = "model_id"

    async def parse_value(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
        raw_value: list[str] | None,
    ) -> list[str]:
        msg = persona_info.message_stripped_str
        value = parse_delimited_string(msg)
        if not value:
            await send_msg.send_error("Please enter at least one model_id")
        return value
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: list[str],
        ):
        await send_msg.send_response_check_code(response, f"Set Multiple Model to {', '.join(value)}")