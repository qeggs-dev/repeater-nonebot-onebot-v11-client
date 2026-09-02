from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from ....command_register import(
    CommandCaller,
    CommandPackage
)
from ....clients import PromptClient

@CommandCaller.register
class RenderPrompt(CommandPackage):
    cmd = "renderPrompt"
    aliases = {
        "rp",
        "RP",
        "render_prompt",
        "Render_Prompt",
        "RenderPrompt",
        "RENDER_PROMPT",
    }
    cmd_type = CmdTypes.PROMPT
    description = f"""
    Preview the prompts submitted to AI.

    Usage:
    ```
    /{cmd}
    ```
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        user_configs = await persona_info.get_user_configs()
        prompt_client = PromptClient(persona_info, user_configs)
        response = await prompt_client.get_prompt()
        if response:
            if response.text:
                await send_msg.send_render_prompt(response.text)
            else:
                await send_msg.send_prompt("[No Prompt]")
        else:
            await send_msg.send_response(response)