from nonebot.adapters.onebot.v11 import Message

from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...client_configs import storage_configs


@CommandCaller.register
class GetCQ(CommandPackage):
    cmd = "getCQ"
    aliases = {
        "gcq",
        "GCQ",
        "get_cq",
        "Get_CQ",
        "GetCQ",
        "GetCQ",
    }
    cmd_type = CmdTypes.SENDMSG
    description = f"""
    Get CQ Message

    Usage:
      /{cmd} message
    """
    super_permissions = True

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if not storage_configs.allow_send_any_message:
            await send_msg.send_error("Send_Message is disabled")
            return
        
        await send_msg.send_text(str(persona_info.message), reply=False)