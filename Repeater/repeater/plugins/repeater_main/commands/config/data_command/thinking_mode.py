from ....assist import PersonaInfo, SendMsg, Response, str_to_bool
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class ThinkingMode(BaseConfig):
    cmd = "thinkingMode"
    aliases = {
        "tm",
        "TM",
        "thinking_mode",
        "Thinking_Mode",
        "ThinkingMode",
        "THINKING_MODE",
    }
    field = "thinking"
    description = f"""
    Turn on the inference mode of hybrid inference model.

    Usage:
      /{cmd} true
      /{cmd} false
    """

    async def parse_value(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
        raw_value: bool | None,
    )  -> bool | None:
        try:
            value = str_to_bool(persona_info.message_stripped_str, optional=True)
        except ValueError:
            await send_msg.send_error("Not a valid value")
        return value
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: bool
        ):
        if value is None:
            mode_str = "default"
        else:
            mode_str = "enabled" if value else "disabled"
        await send_msg.send_response_check_code(response, f"Thinking Mode is {mode_str}")