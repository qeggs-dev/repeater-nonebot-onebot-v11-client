from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...clients import ChatClient


@CommandCaller.register
class GetChatBuffer(CommandPackage):
    cmd = "getChatBuffer"
    aliases = {
        "gcb",
        "GCB",
        "get_chat_buffer",
        "Get_Chat_Buffer",
        "GetChatBuffer",
        "GET_CHAT_BUFFER",
    }
    cmd_type = CmdTypes.STATUS
    description = f"""
    Get the chat buffer of the current chat session.

    Usage:
    ```
    /{cmd} task_id
    ```
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        user_configs = await persona_info.get_user_configs()
        chat_client = ChatClient(persona_info, user_configs)
        response = await chat_client.get_chat_buffer()
        if response:
            buffer_response = response.get_data()
            if buffer_response is None:
                await send_msg.send_error_response(response)
            else:
                if persona_info.message_stripped_str in buffer_response.buffers:
                    buffer = buffer_response.buffers[persona_info.message_stripped_str]
                    await send_msg.send_chat_response(
                        reasoning_content = buffer.reasoning,
                        content = buffer.content
                    )
        
        send_msg.break_handler()