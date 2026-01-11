from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ..._clients import ConfigCore
from ....assist import PersonaInfo, SendMsg

config_branch_binding_from = on_command("configBranchBindingFrom", aliases={"cfgbbf", "config_branch_binding_from", "Config_Branch_Binding_From", "ConfigBranchBindingFrom"}, rule=to_me(), block=True)

@config_branch_binding_from.handle()
async def handle_config_branch_binding_from(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Config_Branch_Binding_From", config_branch_binding_from, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    msg = args.extract_plain_text().strip()
    
    config_core = ConfigCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await config_core.binding_from(msg)
        await send_msg.send_response(response, f"Binding Config Branch from {msg}")