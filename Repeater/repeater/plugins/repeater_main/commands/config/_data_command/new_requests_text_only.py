from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ConfigCore
from ....assist import PersonaInfo, SendMsg, str_to_bool

set_new_requests_text_only = on_command("newRequestsTextOnly", aliases={"nrto", "new_requests_text_only", "New_Requests_Text_Only", "NewRequestsTextOnly"}, rule=to_me(), block=True)

@set_new_requests_text_only.handle()
async def handle_new_requests_text_only(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.New_Requests_Text_Only", set_new_requests_text_only, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    
    try:
        new_requests_text_only = str_to_bool(persona_info.message_str)
    except ValueError:
        await send_msg.send_error("Not a valid boolean value")
    
    config_core = ConfigCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await config_core.set_config("new_requests_text_only", new_requests_text_only)
        await send_msg.send_response_check_code(response, f"Set New Requests Text Only to {new_requests_text_only}")
        
