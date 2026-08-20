from ...clients import ChatClient, ChatSendMsg
from ...assist import PersonaInfo, SendMsg
from ...logger import logger
from ...command_register import CommandCaller
from .._bases import BaseChat

@CommandCaller.register
class ChatKeepReasoning(BaseChat):
    cmd = "keepReasoning"
    aliases = {
        "kr",
        "KR",
        "keep_reasoning",
        "Keep_Reasoning",
        "KeepReasoning",
        "KEEP_REASONING"
    }
    description = f"""
        Let the AI continue generating content and turn on inferential mode. (sending an empty message) 
        
        Usage:
        ```
        /{cmd}
        ```
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        logger.info(
            "Received a message from {namespace}",
            namespace = persona_info.namespace_str,
            module = send_msg.component
        )

        chat_client = await self.get_client(persona_info)

        response = await chat_client.send_message(
            thinking=True,
        )
        
        send_msg = ChatSendMsg(
            send_msg.component,
            persona_info,
            response,
            send_msg.matcher,
        )
        await self.send_chat_send_msg(send_msg)
