from ...assist import PersonaInfo, SendMsg, Response
from ...clients import ChatClient, DataRoutingField, CrossUserDataRouting, ChatResponse
from ...command_register import CommandCaller
from .._bases import BaseChat, SendMessage

@CommandCaller.register
class Reference(BaseChat):
    cmd = "reference"
    aliases = {
        "ref",
        "REF",
        "Reference",
        "REFERENCE"
    }
    description = f"""
        References the Context of other members to generate text
        Note: You Need to ensure that you and the other party, as well as the server, all allow cross-user data access.
        
        Usage:
        ```
        /{cmd} @somebody text
        ```
    """
    
    async def send_message(
        self,
        client: ChatClient,
        send_messages: SendMessage,
        persona_info: PersonaInfo,
        send_msg: SendMsg
    ) -> Response[ChatResponse]:
        if not persona_info.noself_at_list:
            await send_msg.send_error("Please at a member to get reference.")
            
        response = await client.send_message(
            message = send_messages.text,
            cross_user_data_routing = CrossUserDataRouting(
                context = DataRoutingField(
                    load_from_user_id = persona_info.noself_at_list[0]
                )
            ),
            image_url = send_messages.images,
            audio_url = send_messages.audios,
            video_url = send_messages.videos,
            file_url = send_messages.files,
        )

        return response