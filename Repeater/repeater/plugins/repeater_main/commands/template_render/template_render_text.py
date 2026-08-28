from ...assist import PersonaInfo, SendMsg, Response
from ...command_register import CommandCaller
from .template_render import TemplateRender

@CommandCaller.register
class TemplateRenderText(TemplateRender):
    cmd = "templateRenderText"
    aliases = {
        "trt",
        "TRT",
        "template_render_text",
        "Template_Render_Text",
        "TemplateRenderText",
        "TEMPLATE_RENDER_TEXT",

        # Reserved for compatibility.
        "vet",
        "VET",
        "var_expand_text",
        "Var_Expand_Text",
        "VarExpandText",
        "VAR_EXPAND_TEXT",
    }
    description = f"""
    Render a template and .

    Usage:
    ```
    /{cmd} template_text
    ```
    """
    
    async def send_result(self, persona_info: PersonaInfo, send_msg: SendMsg, response: Response[None]):
        if response:
            await send_msg.send_text(response.text)
        else:
            await send_msg.send_response_check_code(response)