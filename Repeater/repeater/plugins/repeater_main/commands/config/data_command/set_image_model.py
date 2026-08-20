from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class SetImageModel(BaseConfig):
    cmd = "setImageModel"
    aliases = {
        "sim",
        "SIM",
        "set_image_model",
        "Set_Image_Model",
        "SetImageModel",
        "SET_IMAGE_MODEL",
    }
    field = "image_model_id"
    description = f"""
    Set up a model for generating images.

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
        await send_msg.send_response_check_code(response, f"Set Image Model to {value}")