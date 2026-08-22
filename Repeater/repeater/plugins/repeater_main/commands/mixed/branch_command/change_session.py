from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from ....command_register import(
    CommandCaller,
    CommandPackage
)
from ....clients import ContextClient, PromptClient, ConfigClient

@CommandCaller.register
class ChangeSession(CommandPackage):
    cmd = "changeSession"
    aliases = {
        "cs",
        "CS",
        "change_session",
        "Change_Session",
        "ChangeSession",
        "CHANGE_SESSION",
    }
    cmd_type = CmdTypes.BRANCH_MIXED

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        user_configs = await persona_info.get_user_configs()
        context_client = ContextClient(persona_info, user_configs)
        prompt_client = PromptClient(persona_info, user_configs)
        config_client = ConfigClient(persona_info, user_configs)
        response_context = await context_client.change_branch(persona_info.message_stripped_str)
        response_prompt = await prompt_client.change_branch(persona_info.message_stripped_str)
        response_config = await config_client.change_branch(persona_info.message_stripped_str)
        await send_msg.send_multiple_responses(
            (response_context, "Context"),
            (response_prompt, "Prompt"),
            (response_config, "Config")
        )