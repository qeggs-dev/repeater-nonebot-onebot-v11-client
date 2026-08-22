from ....assist import PersonaInfo, SendMsg, Response, str_to_bool
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class SetAutoSaveContext(BaseConfig):
    cmd = "setAutoSaveContext"
    aliases = {
        "sasc",
        "SASC",
        "set_auto_save_context",
        "Set_Auto_Save_Context",
        "SetAutoSaveContext",
        "SET_AUTO_SAVE_CONTEXT"
    }
    field = "save_context"
    description = f"""
    Whether to allow the process to save the context.
    Tip: when set to false, RUL is closed and user requests can be processed in parallel.

    Usage:
      /{cmd} true
      /{cmd} false
    """

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
        await send_msg.send_response_check_code(response, f"Auto Save Context set to {value}")