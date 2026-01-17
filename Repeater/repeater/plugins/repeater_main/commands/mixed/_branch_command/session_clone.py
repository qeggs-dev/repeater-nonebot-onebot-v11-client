from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ..._clients import ContextCore, PromptCore, ConfigCore
from ....assist import PersonaInfo, SendMsg

session_branch_clone = on_command("sessionBranchClone", aliases={"sbc", "session_branch_clone", "Session_Branch_Clone", "SessionBranchClone"}, rule=to_me(), block=True)

@session_branch_clone.handle()
async def handle_session_branch_clone(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Session.Session_Branch_Clone", session_branch_clone, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    msg = args.extract_plain_text().strip()
    
    context_core = ContextCore(persona_info)
    prompt_core = PromptCore(persona_info)
    config_core = ConfigCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        context_response = await context_core.clone(msg)
        prompt_response = await prompt_core.clone(msg)
        config_response = await config_core.clone(msg)

        await send_msg.send_multiple_responses(
            (context_response, "Context"),
            (prompt_response, "Prompt"),
            (config_response, "Config"),
        )