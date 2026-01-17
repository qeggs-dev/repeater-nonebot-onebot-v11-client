from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ..._clients import ContextCore
from ....assist import PersonaInfo, SendMsg

context_branch_info = on_command("contextBranchInfo", aliases={"cbi", "context_branch_info", "Context_Branch_Info", "ContextBranchInfo"}, rule=to_me(), block=True)

@context_branch_info.handle()
async def handle_context_branch_info(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Context.Context_Branch_Info", context_branch_info, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    
    context_core = ContextCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await context_core.branch_info()
        if response.code == 200:
            await send_msg.send_prompt(
                f"Branch Type: Context\n"
                f"Branch ID: {response.data.branch_id}\n"
                f"Branch Size: {response.data.size}\n"
                f"Branch Readable Size: {response.data.readable_size}\n"
                f"Branch Create Time: {response.data.created_time().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
        else:
            await send_msg.send_response(response, "Get Context branch info failed")