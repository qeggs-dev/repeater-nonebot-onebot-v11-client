from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ..._clients import ContextCore
from ....assist import PersonaInfo, SendMsg

context_branch_clone = on_command("contextBranchClone", aliases={"cbc", "context_branch_clone", "Context_Branch_Clone", "ContextBranchClone"}, rule=to_me(), block=True)

@context_branch_clone.handle()
async def handle_context_branch_clone(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Context.Context_Branch_Clone", context_branch_clone, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    msg = args.extract_plain_text().strip()
    
    context_core = ContextCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await context_core.clone(msg)
        await send_msg.send_response_check_code(response, f"Clone Context Branch to {msg}")