from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ConfigCore
from ....assist import PersonaInfo, SendMsg

change_config_branch = on_command("changeConfigBranch", aliases={"ccfgb", "change_config_branch", "Change_Config_Branch", "ChangeConfigBranch"}, rule=to_me(), block=True)

@change_config_branch.handle()
async def handle_change_config_branch(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Change_Config_Branch", change_config_branch, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    config_core = ConfigCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await config_core.change_branch(persona_info.message_str)
        await send_msg.send_response_check_code(response, f"Config branch changed to {persona_info.message_str}")