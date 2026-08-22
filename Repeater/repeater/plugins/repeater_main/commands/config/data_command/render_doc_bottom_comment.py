from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class RenderDocBottomComment(BaseConfig):
    cmd = "renderDocBottomComment"
    aliases = {
        "rdbc",
        "RDBC",
        "render_doc_bottom_comment",
        "Render_Doc_Bottom_Comment",
        "RenderDocBottomComment",
        "RENDER_DOC_BOTTOM_COMMENT",
    }
    field = "render_document_bottom_comment"
    description = f"""
    Fixed the content of the comment at the bottom when rendering the image.

    Usage:
      /{cmd} text
    """
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: str
        ):
        await send_msg.send_response_check_code(response, f"Set Render Document Bottom Comments to {value}")