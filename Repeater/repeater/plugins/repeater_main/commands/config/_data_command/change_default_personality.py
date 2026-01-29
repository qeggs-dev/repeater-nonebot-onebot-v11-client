from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ConfigCore
from ....assist import PersonaInfo, SendMsg

change_default_personality = on_command("changeDefaultPersonality", aliases={"cdp", "change_default_personality", "Change_Default_Personality", "ChangeDefaultPersonality"}, rule=to_me(), block=True)

@change_default_personality.handle()
async def handle_change_default_personality(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Change_Default_Personality", change_default_personality, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    
    config_core = ConfigCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await config_core.set_config("parset_prompt_name", persona_info.message_str)
        await send_msg.send_response_check_code(response, f"Change Default Personality to {persona_info.message_str}")
        
