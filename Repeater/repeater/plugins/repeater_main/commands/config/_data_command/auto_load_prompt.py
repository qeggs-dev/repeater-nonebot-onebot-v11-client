from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ConfigCore
from ....assist import PersonaInfo, SendMsg, str_to_bool

set_auto_load_prompt = on_command("setAutoLoadPrompt", aliases={"salp", "set_auto_load_prompt", "Set_Auto_Load_Prompt", "SetAutoLoadPrompt"}, rule=to_me(), block=True)

@set_auto_load_prompt.handle()
async def handle_set_auto_load_prompt(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Set_Auto_Load_Prompt", set_auto_load_prompt, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    try:
        auto_load_prompt = str_to_bool(persona_info.message_str)
    except ValueError:
        await send_msg.send_error("Not a valid boolean value")

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        config_core = ConfigCore(persona_info)
        response = await config_core.set_config("load_prompt", auto_load_prompt)
        await send_msg.send_response_check_code(response, f"Auto Load Prompt set to {auto_load_prompt}")