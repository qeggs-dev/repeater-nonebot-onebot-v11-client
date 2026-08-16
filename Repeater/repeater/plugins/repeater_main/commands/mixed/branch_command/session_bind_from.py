from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from ....command_register import(
    CommandCaller,
    CommandPackage
)
from ....clients import ContextClient, PromptClient, ConfigClient

@CommandCaller.register
class SessionBranchBindFrom(CommandPackage):
    cmd = "sessionBranchBindFrom"
    aliases = {
        "sbbf",
        "SBBF",
        "session_branch_bind_from",
        "Session_Branch_Bind_From",
        "SessionBranchBindFrom",
        "SESSION_BRANCH_BIND_FROM",
    }
    cmd_type = CmdTypes.BRANCH_MIXED

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        msg = persona_info.message_stripped_str

        user_configs = await persona_info.get_user_configs()
        context_client = ContextClient(persona_info, user_configs)
        prompt_client = PromptClient(persona_info, user_configs)
        config_client = ConfigClient(persona_info, user_configs)
        context_response = await context_client.bind_from(msg)
        prompt_response = await prompt_client.bind_from(msg)
        config_response = await config_client.bind_from(msg)

        await send_msg.send_multiple_responses(
            (context_response, "Context"),
            (prompt_response, "Prompt"),
            (config_response, "Config"),
        )   