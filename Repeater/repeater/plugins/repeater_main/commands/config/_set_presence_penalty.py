from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from .._clients import ConfigCore
from ...assist import PersonaInfo, SendMsg

set_presence_penalty = on_command("setPresencePenalty", aliases={"spp", "set_presence_penalty", "Set_Presence_Penalty", "SetPresencePpenalty"}, rule=to_me(), block=True)

@set_presence_penalty.handle()
async def handle_set_presence_penalty(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Set_Presence_Penalty", set_presence_penalty, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    msg = persona_info.message_str.strip()

    try:
        if msg.endswith("%"):
            msg = msg[:-1]
            presence_penalty = float(msg) / 100
        else:
            presence_penalty = float(msg)
    except ValueError:
        await send_msg.send_error("Presence_Penalty is set incorrectly. Please enter a floating-point number or percentage between -2 and 2!")
    if presence_penalty < -2 or presence_penalty > 2:
        await send_msg.send_error("Presence_Penalty is set incorrectly. Please enter a floating-point number or percentage between -2 and 2!")


    config_core = ConfigCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await config_core.set_config("presence_penalty", presence_penalty)
        await send_msg.send_response(response, f"Set Presence_Penalty to {presence_penalty}")