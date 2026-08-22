from ...clients import ChatClient, ChatResponse
from ...command_register import CommandCaller
from .._bases import BaseChat, SendMessage
from ...assist import PersonaInfo, SendMsg, Response

@CommandCaller.register
class NoReason(BaseChat):
    cmd = "noReason"
    aliases = {
        "nr",
        "NR",
        "no_reason",
        "No_Reason",
        "NoReason",
        "NO_REASON"
    }
    description = f"""
        Forces the use of non-inferential mode for text generation.
        
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
            thinking = False
        )
        return response