from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from .._clients import ContextCore
from ...assist import PersonaInfo, SendMsg

delcontext = on_command("deleteContext", aliases={"dc", "delete_context", "Delete_Context", "DeleteContext"}, rule=to_me(), block=True)

@delcontext.handle()
async def handle_delete_context(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Context.Delete_Context", delcontext, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    
    context_core = ContextCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await context_core.delete_context()
        await send_msg.send_response(response, f"Delete Context from {persona_info.namespace_str}")