from nonebot import logger
from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....command_register import(
    CommandCaller
)
from ....clients import ChatResponse, ChatClient
from ..._bases import BaseChat, SendMessage
from ...context.data_command.withdraw import Withdraw

@CommandCaller.register
class Rewrite(BaseChat):
    cmd = "rewrite"
    aliases = {
        "rew",
        "REW",
        "Rewrite",
        "REWRITE",
    }
    cmd_type = CmdTypes.MIXED
    documents = """
        Withdraw and send with new content.
    """

    async def send_message(
        self,
        client: ChatClient,
        send_messages: SendMessage,
        persona_info: PersonaInfo,
        send_msg: SendMsg
    ) -> Response[ChatResponse]:
        package = CommandCaller.get_instance(Withdraw)
        await CommandCaller.horizontal_call(
            package,
            persona_info,
            send_msg = send_msg.copy(
                component = package.component
            )
        )
        
        return await super().send_message(
            client,
            send_messages,
            persona_info,
            send_msg
        )