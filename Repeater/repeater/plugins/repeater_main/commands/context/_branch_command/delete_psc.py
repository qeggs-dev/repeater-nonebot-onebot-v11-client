from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ContextCore
from ....assist import PersonaInfo, SendMsg

delete_public_space_context = on_command("deletePublicSpaceContext", aliases={"dpsc", "delete_public_space_context", "Delete_Public_Space_Context", "DeletePublicSpaceContext"}, rule=to_me(), block=True)

@delete_public_space_context.handle()
async def handle_delete_public_space_context(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Context.Delete_Public_Space_Context", delete_public_space_context, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    context_core = ContextCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await context_core.delete()
        await send_msg.send_response_check_code(response, f"Delete Public Space Context from {persona_info.namespace_str}")