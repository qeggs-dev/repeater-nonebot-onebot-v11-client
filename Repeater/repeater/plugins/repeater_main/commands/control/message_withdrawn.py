from typing import Any, Type
from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from nonebot.exception import ActionFailed

@CommandCaller.register
class MessageWithdrawn(CommandPackage):
    cmd = "messageWithdrawn"
    aliases = {
        "mw",
        "MW",
        "message_withdrawn",
        "Message_Withdrawn",
        "MessageWithdrawn",
        "MESSAGE_WITHDRAWN"
    }
    cmd_type = CmdTypes.CONTROL
    description = f"""
        Withdrawn a droid's own message.

        Usage:
        > Reply to a message with

        ```
        /{cmd}
        ```
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):

        reply  = await persona_info.from_reply()
        if reply is None:
            await send_msg.send_error("No message to withdraw.")
            return
        
        if not reply.is_self:
            await send_msg.send_error("You can only withdraw your own messages.")
            return
        
        # Call API
        try:
            await reply.cached_api.delete_msg(message_id = reply.message_id)
        except ActionFailed as e:
            await send_msg.send_error(f"Failed to withdraw message: {e}")
            return
        
        await send_msg.send_prompt("Message withdrawn.")