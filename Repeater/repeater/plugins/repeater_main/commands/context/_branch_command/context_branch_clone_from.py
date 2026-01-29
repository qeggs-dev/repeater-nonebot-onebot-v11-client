from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ..._clients import ContextCore
from ....assist import PersonaInfo, SendMsg

context_branch_clone_from = on_command("contextBranchCloneFrom", aliases={"cbcf", "context_branch_clone_from", "Context_Branch_Clone_From", "ContextBranchCloneFrom"}, rule=to_me(), block=True)

@context_branch_clone_from.handle()
async def handle_context_branch_clone_from(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Context.Context_Branch_Clone_From", context_branch_clone_from, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    msg = args.extract_plain_text().strip()
    
    context_core = ContextCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await context_core.clone_from(msg)
        await send_msg.send_response_check_code(response, f"Clone Context Branch from {msg}")