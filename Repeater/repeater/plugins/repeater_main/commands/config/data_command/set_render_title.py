from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class SetRenderTitle(BaseConfig):
    cmd = "setRenderTitle"
    aliases = {
        "srt",
        "SRT",
        "set_render_title",
        "Set_Render_Title",
        "SetRenderTitle",
        "SET_RENDER_TITLE",
    }
    field = "render_title"
    description = f"""
    Sets a caption that is fixed at the top of the image during rendering.

    Usage:
      /{cmd} title
    """

    # 字符串类型，不需要重写 parse_value
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: str
        ):
        await send_msg.send_response_check_code(response, f"Set Render_Title to {value}")