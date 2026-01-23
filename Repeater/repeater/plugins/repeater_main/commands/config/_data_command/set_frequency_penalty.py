from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ConfigCore
from ....assist import PersonaInfo, SendMsg

set_frequency_penalty = on_command("setFrequencyPenalty", aliases={"sfp", "set_frequency_penalty", "Set_Frequency_Penalty", "SetFrequencyPenalty"}, rule=to_me(), block=True)

@set_frequency_penalty.handle()
async def handle_set_frequency_penalty(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)
    send_msg = SendMsg("Config.Set_Frequency_Penalty", set_frequency_penalty, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    msg = persona_info.message_str

    try:
        if msg.endswith("%"):
            msg = msg[:-1]
            frequency_penalty = float(msg) / 100
        else:
            frequency_penalty = float(msg)
    except ValueError:
        await send_msg.send_error("Frequency_Penalty setting is incorrect, please enter a floating-point number or percentage between -2 and 2!")
    if frequency_penalty < -2 or frequency_penalty > 2:
        await send_msg.send_error("Frequency_Penalty setting is incorrect, please enter a floating-point number or percentage between -2 and 2!")


    config_core = ConfigCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await config_core.set_config("frequency_penalty", frequency_penalty)
        await send_msg.send_response_check_code(response, f"Set Frequency_Penalty to {frequency_penalty}")
        