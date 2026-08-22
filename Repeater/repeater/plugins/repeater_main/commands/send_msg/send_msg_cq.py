from nonebot.adapters.onebot.v11 import Message

from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...client_configs import storage_configs


@CommandCaller.register
class SendMessageCQ(CommandPackage):
    cmd = "sendMessageCQ"
    aliases = {
        "smsgcq",
        "SMSGCQ",
        "send_message_cq",
        "Send_Message_CQ",
        "SendMessageCQ",
        "SEND_MESSAGE_CQ",
    }
    cmd_type = CmdTypes.SENDMSG
    description = f"""
    Send an arbitrary Onebot cq message.

    Usage:
      /{cmd} cq_message
    """
    superuser_permissions = True

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if not storage_configs.allow_send_any_message:
            await send_msg.send_error("Send_Message is disabled")
            return

        message = Message(persona_info.message_stripped_str)

        await send_msg.send_any(message, reply=False)