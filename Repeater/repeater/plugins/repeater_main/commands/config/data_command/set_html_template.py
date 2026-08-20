from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class SetHtmlTemplate(BaseConfig):
    cmd = "setHtmlTemplate"
    aliases = {
        "sht",
        "SHT",
        "set_html_template",
        "Set_Html_Template",
        "SetHtmlTemplate",
        "SET_HTML_TEMPLATE",
    }
    field = "render_html_template"
    description = f"""
    Set the HTML Template name to use when rendering.

    Usage:
      /{cmd} html_template_name
    """
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: str
        ):
        await send_msg.send_response_check_code(response, f"Set Html Template to {value}")