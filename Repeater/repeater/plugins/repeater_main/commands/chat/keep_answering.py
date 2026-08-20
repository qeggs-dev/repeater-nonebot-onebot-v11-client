from ...clients import ChatClient, ChatSendMsg
from ...assist import PersonaInfo, SendMsg
from ...logger import logger
from ...command_register import CommandCaller
from .._bases import BaseChat

@CommandCaller.register
class ChatKeepAnswering(BaseChat):
    cmd = "keepAnswering"
    aliases = {
        "ka",
        "KA",
        "keep_answering",
        "Keep_Answering",
        "KeepAnswering",
        "KEEP_ANSWERING"
    }
    description = f"""
        Let the AI continue generating content. (sending an empty message) 
        
        Usage:
        ```
        /{cmd}
        ```
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        logger.info(
            "Received a message from {namespace}",
            namespace=persona_info.namespace_str,
            module = send_msg.component
        )

        chat_client = await self.get_client(persona_info)

        response = await chat_client.send_message()
        
        send_msg = ChatSendMsg(
            send_msg.component,
            persona_info,
            response,
            send_msg.matcher,
        )
        await send_msg.send()