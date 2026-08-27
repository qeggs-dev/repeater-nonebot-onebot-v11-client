from ...assist import PersonaInfo, SendMsg, Response
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...clients import TemplateRenderClient

@CommandCaller.register
class TemplateRender(CommandPackage):
    cmd = "templateRender"
    aliases = {
        "tr",
        "TR",
        "template_render",
        "Template_Render",
        "TemplateRender",
        "TEMPLATE_RENDER",

        # Reserved for compatibility.
        "varExpand",
        "ve",
        "VE",
        "var_expand",
        "Var_Expand",
        "VarExpand",
        "VAR_EXPAND",
    }
    cmd_type = CmdTypes.TEMPLATE
    description = f"""
    Render a template.

    Usage:
    ```
    /{cmd} template_text
    ```
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        msg = persona_info.message_stripped_str
        user_configs = await persona_info.get_user_configs()
        variable_expansion_client = TemplateRenderClient(persona_info, user_configs)
        response = await variable_expansion_client.render(text = msg)
        await self.send_result(persona_info, send_msg, response)
    
    async def send_result(self, persona_info: PersonaInfo, send_msg: SendMsg, response: Response[None]):
        if response:
            await send_msg.send_check_length(response.text)
        else:
            await send_msg.send_response_check_code(response)