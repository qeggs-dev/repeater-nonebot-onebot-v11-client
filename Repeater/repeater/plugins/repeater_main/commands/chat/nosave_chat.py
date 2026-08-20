from ...clients import ChatClient, ChatResponse
from ...command_register import CommandCaller
from .._bases import BaseChat, SendMessage
from ...assist import PersonaInfo, SendMsg, Response

@CommandCaller.register
class NoSaveChat(BaseChat):
    cmd = "noSaveChat"
    aliases = {
        "nsc",
        "NSC",
        "no_save_chat",
        "NoSaveChat",
        "No_Save_Chat",
        "NO_SAVE_CHAT"
    }
    description = f"""
        Temporarily send a message. (Not saved in the chat history)
        
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
            save_context = False
        )
        return response