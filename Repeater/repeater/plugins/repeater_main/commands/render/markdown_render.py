from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)


@CommandCaller.register
class MarkdownRender(CommandPackage):
    cmd = "markdownRender"
    aliases = {
        "mr",
        "MR",
        "markdown_render",
        "Markdown_Render",
        "MarkdownRender",
        "MARKDOWN_RENDER",
    }
    cmd_type = CmdTypes.RENDER

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        await send_msg.send_render(persona_info.message_stripped_str)