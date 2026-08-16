from ....assist import PersonaInfo, SendMsg, Response, str_to_bool
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class RemoveReasoningPrompt(BaseConfig):
    cmd = "removeReasoningPrompt"
    aliases = {
        "rrp",
        "RRP",
        "remove_reasoning_prompt",
        "Remove_Reasoning_Prompt",
        "RemoveReasoningPrompt",
        "REMOVE_REASONING_PROMPT",
    }
    field = "remove_reasoning_prompt"

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
        await send_msg.send_response_check_code(response, f"Set Remove Reasoning Prompt to {value}")