from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ConfigCore
from ....assist import PersonaInfo, SendMsg

set_temperature = on_command("setTemperature", aliases={"st", "set_temperature", "Set_Temperature", "SetTemperature"}, rule=to_me(), block=True)

@set_temperature.handle()
async def handle_set_temperature(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Set_Temperature", set_temperature, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    msg = persona_info.message_str.strip()

    try:
        if msg.endswith("%"):
            msg = msg[:-1]
            temperature = (float(msg) / 100)
        else:
            temperature = float(msg)
    except ValueError:
        await send_msg.send_error("Temperature is set incorrectly. Please enter a floating-point number or percentage between 0 and 2!")
    if temperature < 0 or temperature > 2:
        await send_msg.send_error("Temperature is set incorrectly. Please enter a floating-point number or percentage between 0 and 2!")

    config_core = ConfigCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await config_core.set_config("temperature", temperature)
        await send_msg.send_response(response, f"Set Temperature to {temperature}")