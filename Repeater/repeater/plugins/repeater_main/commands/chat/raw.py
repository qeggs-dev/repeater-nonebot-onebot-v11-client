from ...clients import ChatClient, ChatResponse
from ...command_register import CommandCaller
from .._bases import BaseChat, SendMessage
from ...assist import PersonaInfo, SendMsg, Response

@CommandCaller.register
class RawChat(BaseChat):
    cmd = "raw"
    aliases = {
        "RAW",
        "rawchat",
        "raw_chat",
        "Raw_Chat",
        "RawChat",
        "RAW_CHAT"
    }
    description = f"""
        Generates text without adding metadata.
        
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
            raw_message = True
        )
        return response