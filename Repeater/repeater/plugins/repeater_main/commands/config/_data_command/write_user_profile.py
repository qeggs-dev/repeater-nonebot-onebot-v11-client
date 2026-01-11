from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ConfigCore
from ....assist import PersonaInfo, SendMsg, str_to_bool

write_user_profile = on_command("writeUserProfile", aliases={"wup", "write_user_profile", "Write_User_Profile", "WriteUserProfile"}, rule=to_me(), block=True)

@write_user_profile.handle()
async def handle_write_user_profile(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Write_User_Profile", write_user_profile, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        config_core = ConfigCore(persona_info)
        response = await config_core.set_config("user_profile", persona_info.message_str)
        await send_msg.send_response(response, f"Write_User_Profile seted")