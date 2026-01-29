from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ConfigCore
from ....assist import PersonaInfo, SendMsg, str_to_bool

set_cross_user_data_access = on_command("crossUserDataAccess", aliases={"cuda", "cross_user_data_access", "Cross_User_Data_Access", "CrossUserDataAccess"}, rule=to_me(), block=True)

@set_cross_user_data_access.handle()
async def handle_cross_user_data_access(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Cross_User_Data_Access", set_cross_user_data_access, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    
    try:
        cross_user_data_access = str_to_bool(persona_info.message_str)
    except ValueError:
        await send_msg.send_error("Not a valid boolean value")
    
    config_core = ConfigCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await config_core.set_config("cross_user_data_access", cross_user_data_access)
        await send_msg.send_response_check_code(response, f"Set Cross User Data Access to {cross_user_data_access}")
        
