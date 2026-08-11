from ...clients import ChatClient, ChatResponse
from ...command_register import CommandCaller
from .._bases import BaseChat, SendMessage
from ...assist import PersonaInfo, SendMsg, Response

@CommandCaller.register
class SummarizeAndContract(BaseChat):
    cmd = "summarizeAndContract"
    aliases = {
        "sac",
        "SAC",
        "summarize_and_contract",
        "Summarize_And_Contract",
        "SummarizeAndContract",
        "SUMARAIZE_AND_CONTRACT"
    }
    documents = f"""
        Summarizes the user's contextual content
        And save only summary information

        Usage:
        ```
        /{cmd} [message]
        ```
    """
    
    async def send_message(
        self,
        client: ChatClient,
        send_messages: SendMessage,
        persona_info: PersonaInfo,
        send_msg: SendMsg
    ) -> Response[ChatResponse]:
        if not send_messages.text:
            await send_msg.send_error("Please provide a message to summarize")
        response = await client.send_message(
            message = send_messages.text,
            image_url = send_messages.images,
            audio_url = send_messages.audios,
            video_url = send_messages.videos,
            file_url = send_messages.files,
            save_new_only = True
        )
        return response