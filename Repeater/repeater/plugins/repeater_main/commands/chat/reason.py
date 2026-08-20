from ...clients import ChatClient, ChatResponse
from ...command_register import CommandCaller
from .._bases import BaseChat, SendMessage
from ...assist import PersonaInfo, SendMsg, Response

@CommandCaller.register
class Reason(BaseChat):
    cmd = "reason"
    aliases = {
        "r",
        "R",
        "Reason",
        "REASON"
    }
    description = f"""
        The inference mode is forced to be turned on for this text generation task.
        
        Usage:
        ```
        /{cmd} text
        ```
    """
    
    async def send_message(
        self,
        client: ChatClient,
        send_messages: SendMessage,
        persona_info: PersonaInfo,
        send_msg: SendMsg
    ) -> Response[ChatResponse]:
        response = await client.send_message(
            message = send_messages.text,
            image_url = send_messages.images,
            audio_url = send_messages.audios,
            video_url = send_messages.videos,
            file_url = send_messages.files,
            thinking = True
        )
        return response