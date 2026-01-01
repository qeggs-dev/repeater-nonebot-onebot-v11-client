from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from .._clients import ConfigCore
from ...assist import PersonaInfo, SendMsg

del_config = on_command("delConfig", aliases={"dcfg", "delete_config", "Delete_Config", "DeleteConfig"}, rule=to_me(), block=True)

@del_config.handle()
async def handle_del_config(bot: Bot, event: MessageEvent):
    persona_info = PersonaInfo(bot, event)
    send_msg = SendMsg("Config.Delete_Config", del_config, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    config_core = ConfigCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await config_core.delete_config()
        await send_msg.send_response(response, f"Delete Config {persona_info.namespace_str}")
