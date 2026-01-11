from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ..._clients import ContextCore
from ....assist import PersonaInfo, SendMsg

context_branch_binding_from = on_command("contextBranchBindingFrom", aliases={"cbcf", "context_branch_binding_from", "Context_Branch_Binding_From", "ContextBranchBindingFrom"}, rule=to_me(), block=True)

@context_branch_binding_from.handle()
async def handle_context_branch_binding_from(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Context.Context_Branch_Binding_From", context_branch_binding_from, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    msg = args.extract_plain_text().strip()
    
    context_core = ContextCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await context_core.binding_from(msg)
        await send_msg.send_response(response, f"Binding Context Branch from {msg}")