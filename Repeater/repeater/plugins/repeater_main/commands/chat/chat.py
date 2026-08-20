from .._bases import BaseChat
from ...clients import ChatSendMsg
from ...command_register import CommandCaller, CommandPackage

@CommandCaller.register
class Chat(BaseChat):
    cmd = "chat"
    aliases = {
        "c",
        "C",
        "Chat",
        "CHAT"
    }
    description = f"""
        Initiates a text generation request
        Return content to force text output.
        
        Usage:
        ```
        /{cmd} text
        ```
    """

    async def send_chat_send_msg(
        self,
        chat_send_msg: ChatSendMsg,
    ):
        await chat_send_msg.send_text_mode()