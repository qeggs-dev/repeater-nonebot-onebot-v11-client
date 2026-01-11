from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ConfigCore
from ....assist import PersonaInfo, SendMsg

set_max_tokens = on_command("setMaxTokens", aliases={"smt", "set_max_tokens", "Set_Max_Tokens", "SetMaxTokens"}, rule=to_me(), block=True)

@set_max_tokens.handle()
async def handle_set_max_tokens(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Set_Max_Tokens", persona_info, set_max_tokens, None)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    msg = persona_info.message_str.strip()

    try:
        max_tokens = int(msg)
    except ValueError:
        await send_msg.send_error("Max_Tokens setting is incorrect, please enter an integer!")
        
    if max_tokens < 1 or max_tokens > 8192:
        await send_msg.send_error("Max_Tokens setting is incorrect, please enter an integer between 1 and 8192!")


    config_core = ConfigCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await config_core.set_config("max_tokens", max_tokens)
        await send_msg.send_response(response, f"Set Max_Tokens to {max_tokens}")