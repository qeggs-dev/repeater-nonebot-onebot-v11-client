from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from ....command_register import(
    CommandCaller,
    CommandPackage
)
from ....clients import ContextClient, ContentRole, ContentUnit


@CommandCaller.register
class InjectSystemContent(CommandPackage):
    cmd = "injectSystemContent"
    aliases = {
        "isc",
        "ISC",
        "inject_system_content",
        "Inject_System_Content",
        "InjectSystemContent",
        "INJECT_SYSTEM_CONTENT",
    }
    cmd_type = CmdTypes.CONTEXT

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        user_config = await persona_info.get_user_configs()
        context_client = ContextClient(persona_info, user_config)
        response = await context_client.inject_context(
            content_unit=ContentUnit(
                content=persona_info.message_stripped_str,
                role=ContentRole.SYSTEM
            )
        )

        if response:
            await send_msg.send_response(
                response,
                message="Inject System Content Successful"
            )
        else:
            await send_msg.send_response(
                response,
                message="Inject System Content Failed"
            )