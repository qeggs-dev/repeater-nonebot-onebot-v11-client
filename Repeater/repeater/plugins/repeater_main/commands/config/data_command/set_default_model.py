from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class SetDefaultModel(BaseConfig):
    cmd = "setDefaultModel"
    aliases = {
        "sdm",
        "SDM",
        "set_default_model",
        "Set_Default_Model",
        "SetDefaultModel",
        "SET_DEFAULT_MODEL",
    }
    field = "model_id"
    description = f"""
    Set a default model for chat.

    Usage:
      /{cmd} model_id
    """
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: str
        ):
        await send_msg.send_response_check_code(response, f"Set Default Model to {value}")