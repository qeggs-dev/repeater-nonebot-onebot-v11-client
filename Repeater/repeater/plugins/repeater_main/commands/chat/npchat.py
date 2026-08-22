from ...clients import ChatClient, ChatResponse
from .._bases import BaseChat, SendMessage
from ...command_register import CommandCaller
from ...assist import PersonaInfo, SendMsg, Response

@CommandCaller.register
class NPChat(BaseChat):
    cmd = "npChat"
    aliases = {
        "np",
        "NP",
        "no_prompt_chat",
        "No_Prompt_Chat",
        "NoPromptChat",
        "NO_PROMPT_CHAT"
    }
    description = f"""
        Generate the task without loading the prompt.
        
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
        response: Response[ChatResponse] = await client.send_message(
            message = send_messages.text,
            image_url = send_messages.images,
            audio_url = send_messages.audios,
            video_url = send_messages.videos,
            file_url = send_messages.files,
            load_prompt = False
        )
        return response