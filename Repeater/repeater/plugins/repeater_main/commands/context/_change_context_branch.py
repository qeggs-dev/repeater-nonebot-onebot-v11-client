from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from .._clients import ContextCore
from ...assist import PersonaInfo, SendMsg

change_context_branch = on_command("changeContextBranch", aliases={"ccb", "change_context_branch", "Change_Context_Branch", "ChangeContextBranch"}, rule=to_me(), block=True)

@change_context_branch.handle()
async def handle_change_context_branch(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Context.Change_Context_Branch", change_context_branch, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    
    msg = persona_info.message_str.strip()
    
    context_core = ContextCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await context_core.change_context_branch(msg)
        await send_msg.send_response(response, f"Change Context Branch to {msg}")