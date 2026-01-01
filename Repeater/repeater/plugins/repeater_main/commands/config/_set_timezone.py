from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from .._clients import ConfigCore
from ...assist import PersonaInfo, SendMsg

set_timezone = on_command("setTimezone", aliases={"stz", "set_timezone", "Set_Timezone", "SetTimezone"}, rule=to_me(), block=True)

@set_timezone.handle()
async def handle_set_timezone(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Set_Timezone", set_timezone, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    msg = persona_info.message_str.strip()

    try:
        timezone = float(msg)
    except ValueError:
        await send_msg.send_error("Invalid timezone value. Please enter a valid number.")
    
    if timezone <= -12 or timezone >= 14:
        await send_msg.send_error("Invalid timezone value. Please enter a number between -12 and 14.")

    config_core = ConfigCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await config_core.set_config("timezone", timezone)
        await send_msg.send_response(response, f"Set Timezone to {timezone}")