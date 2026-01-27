from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ..assist import PersonaInfo, SendMsg
from ._clients import VersionAPICore
from .._adaptation_info import __adaptation__

adaptation_info = on_command("adaptationInfo", aliases={"adai", "adaptation_info", "Adaptation_Info", "AdaptationInfo"}, rule=to_me(), block=True)

@adaptation_info.handle()
async def handle_adaptation(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)
    send_msg = SendMsg("Version.Adaptation_Info", adaptation_info, persona_info)
    version_core = VersionAPICore()

    if send_msg.is_debug_mode:
        send_msg.send_debug_mode()
    else:
        server_version = await version_core.get_version()
        version_data = server_version.get_data()
        if version_data is None:
            send_msg.send_error("Server Version Data is Invalid")
        send_msg.send_prompt(
            (
                f"Client Adaptation Version: {__adaptation__}\n"
                f"Server Core Version: {version_data.core}\n"
                f"Server API Version: {version_data.api}\n"
            )
        )