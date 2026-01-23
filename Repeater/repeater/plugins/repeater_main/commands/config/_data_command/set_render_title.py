from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ConfigCore
from ....assist import PersonaInfo, SendMsg

set_render_title = on_command("setRenderTitle", aliases={"srt", "set_render_title", "Set_Render_Title", "SetRenderTitle"}, rule=to_me(), block=True)

@set_render_title.handle()
async def handle_set_render_title(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Set_Render_Title", set_render_title, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    msg = persona_info.message_str.strip()

    config_core = ConfigCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await config_core.set_config("render_title", msg)
        await send_msg.send_response_check_code(response, f"Set Render_Title to {msg}")