from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ConfigCore
from ....assist import PersonaInfo, SendMsg

set_auto_shrink_length = on_command("setAutoShrinkLength", aliases={"sasl", "set_auto_shrink_length", "Set_Auto_Shrink_Length", "SetAutoShrinkLength"}, rule=to_me(), block=True)

@set_auto_shrink_length.handle()
async def handle_set_auto_shrink_length(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Set_Auto_Shrink_Length", set_auto_shrink_length, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    try:
        auto_shrink_length = int(persona_info.message_str)
    except ValueError:
        await send_msg.send_error("Message must be a number")

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        config_core = ConfigCore(persona_info)
        response = await config_core.set_config("context_shrink_limit", auto_shrink_length)
        await send_msg.send_response_check_code(response, f"Auto shrink length set to {auto_shrink_length}")