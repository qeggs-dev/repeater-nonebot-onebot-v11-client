from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from ....command_register import(
    CommandCaller,
    CommandPackage
)
from ....clients import PromptClient

@CommandCaller.register
class GetPrompt(CommandPackage):
    cmd = "getPrompt"
    aliases = {
        "gp",
        "GP",
        "get_prompt",
        "Get_Prompt",
        "GetPrompt",
        "GET_PROMPT",
    }
    cmd_type = CmdTypes.PROMPT
    description = f"""
    View your own custom prompts.

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