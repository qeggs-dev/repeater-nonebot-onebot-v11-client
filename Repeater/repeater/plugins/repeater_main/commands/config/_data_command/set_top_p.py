from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ConfigCore
from ....assist import PersonaInfo, SendMsg

set_top_p = on_command("setTopP", aliases={"stp", "set_top_p", "Set_Top_P", "SetTopP"}, rule=to_me(), block=True)

@set_top_p.handle()
async def handle_set_top_p(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Set_Top_P", set_top_p, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    msg = persona_info.message_str.strip()

    try:
        if msg.endswith("%"):
            msg = msg[:-1]
            top_p = float(msg) / 100
        else:
            top_p = float(msg)
    except ValueError:
        await send_msg.send_error("Top_P setting error, please enter a floating-point number or percentage between 0 and 1!")
    if top_p < -2 or top_p > 2:
        await send_msg.send_error("Top_P setting error, please enter a floating-point number or percentage between 0 and 1!")

    config_core = ConfigCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await config_core.set_config("top_p", top_p)

        await send_msg.send_response_check_code(response, f"Set Top_P to {top_p}")