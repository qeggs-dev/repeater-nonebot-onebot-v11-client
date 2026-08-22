from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from ....command_register import(
    CommandCaller,
    CommandPackage
)
from ....clients import ContextClient, PromptClient, ConfigClient


@CommandCaller.register
class SessionBranchClone(CommandPackage):
    cmd = "sessionBranchClone"
    aliases = {
        "sbc",
        "SBC",
        "session_branch_clone",
        "Session_Branch_Clone",
        "SessionBranchClone",
        "SESSION_BRANCH_CLONE",
    }
    cmd_type = CmdTypes.BRANCH_MIXED

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        msg = persona_info.message_stripped_str

        user_configs = await persona_info.get_user_configs()
        context_client = ContextClient(persona_info, user_configs)
        prompt_client = PromptClient(persona_info, user_configs)
        config_client = ConfigClient(persona_info, user_configs)
        context_response = await context_client.clone(msg)
        prompt_response = await prompt_client.clone(msg)
        config_response = await config_client.clone(msg)

        await send_msg.send_multiple_responses(
            (context_response, "Context"),
            (prompt_response, "Prompt"),
            (config_response, "Config"),
        )