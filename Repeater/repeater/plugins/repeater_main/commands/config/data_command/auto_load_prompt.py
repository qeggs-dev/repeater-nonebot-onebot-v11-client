from ....assist import PersonaInfo, SendMsg, Response, str_to_bool
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class SetAutoLoadPrompt(BaseConfig):
    cmd = "setAutoLoadPrompt"
    aliases = {
        "salp",
        "SALP",
        "set_auto_load_prompt",
        "Set_Auto_Load_Prompt",
        "SetAutoLoadPrompt",
        "SET_AUTO_LOAD_PROMPT",
    }
    field = "load_prompt"

    async def parse_value(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
        raw_value: bool | None,
    )  -> bool:
        try:
            value = str_to_bool(persona_info.message_stripped_str)
        except ValueError:
            await send_msg.send_error("Not a valid boolean value")
        return value
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: bool
        ):
        await send_msg.send_response_check_code(response, f"Auto Load Prompt set to {value}")