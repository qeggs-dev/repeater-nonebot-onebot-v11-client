from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from ....command_register import(
    CommandCaller,
    CommandPackage
)
from ....clients import ContextClient, PromptClient, ConfigClient


@CommandCaller.register
class SessionBranchBind(CommandPackage):
    cmd = "sessionBranchBind"
    aliases = {
        "sbb",
        "SBB",
        "session_branch_bind",
        "Session_Branch_Bind",
        "SessionBranchBind",
        "SESSION_BRANCH_BIND",
    }
    cmd_type = CmdTypes.BRANCH_MIXED

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        msg = persona_info.message_stripped_str

        user_configs = await persona_info.get_user_configs()
        context_client = ContextClient(persona_info, user_configs)
        prompt_client = PromptClient(persona_info, user_configs)
        config_client = ConfigClient(persona_info, user_configs)
        context_response = await context_client.bind(msg)
        prompt_response = await prompt_client.bind(msg)
        config_response = await config_client.bind(msg)

        await send_msg.send_multiple_responses(
            (context_response, "Context"),
            (prompt_response, "Prompt"),
            (config_response, "Config"),
        )
