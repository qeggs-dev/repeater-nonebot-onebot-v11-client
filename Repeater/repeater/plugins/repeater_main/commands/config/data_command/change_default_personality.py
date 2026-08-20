from ....assist import PersonaInfo, SendMsg, Response
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class ChangeDefaultPersonality(BaseConfig):
    cmd = "changeDefaultPersonality"
    aliases = {
        "cdp",
        "CDP",
        "change_default_personality",
        "Change_Default_Personality",
        "ChangeDefaultPersonality",
        "CHANGE_DEFAULT_PERSONALITY"
    }
    field = "preset_prompt_name"
    description = f"""
    Sets the default personality for the system.

    Usage:
      /{cmd} prompt_postion
    """

    async def parse_value(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
        raw_value: str | None,
    )  -> str:
        return persona_info.message_stripped_str
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: str
        ):
        await send_msg.send_response_check_code(response, f"Change Default Personality to {value}")