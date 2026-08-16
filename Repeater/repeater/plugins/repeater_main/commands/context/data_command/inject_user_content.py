from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from ....command_register import(
    CommandCaller,
    CommandPackage
)
from ....clients import ContextClient, ContentRole, ContentUnit

@CommandCaller.register
class InjectUserContent(CommandPackage):
    cmd = "injectUserContent"
    aliases = {
        "iuc",
        "IUC",
        "inject_user_content",
        "Inject_User_Content",
        "InjectUserContent",
        "INJECT_USER_CONTENT",
    }
    cmd_type = CmdTypes.CONTEXT

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        user_config = await persona_info.get_user_configs()
        context_client = ContextClient(persona_info, user_config)
        response = await context_client.inject_context(
            content_unit=ContentUnit(
                content=persona_info.message_stripped_str,
                role=ContentRole.USER
            )
        )

        if response:
            await send_msg.send_response(
                response,
                message="Inject User Content Successful"
            )
        else:
            await send_msg.send_response(
                response,
                message="Inject User Content Failed"
            )