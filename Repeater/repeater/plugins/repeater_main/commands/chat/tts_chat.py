from .._bases import BaseChat
from ...clients import ChatSendMsg
from ...command_register import CommandCaller

@CommandCaller.register
class TTSChat(BaseChat):
    cmd = "tts_chat"
    aliases = {
        "ttsc",
        "TTSC",
        "tts_Chat",
        "TTS_Chat",
        "TTSChat",
        "TTS_CHAT",
    }
    description = f"""
        Initiates a text generation request,
        Return content to force tts output.
        
        Usage:
        ```
        /{cmd} text
        ```
    """

    async def send_chat_send_msg(
        self,
        chat_send_msg: ChatSendMsg,
    ):
        await chat_send_msg.send_tts_mode()