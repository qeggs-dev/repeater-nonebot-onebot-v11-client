from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ..._clients import ContextCore, PromptCore, ConfigCore
from ....assist import PersonaInfo, SendMsg

session_branch_bind_from = on_command("sessionBranchBindFrom", aliases={"sbbf", "session_branch_bind_from", "Session_Branch_Bind_From", "SessionBranchBindFrom"}, rule=to_me(), block=True)

@session_branch_bind_from.handle()
async def handle_session_branch_bind_from(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Session.Session_Branch_Bind_From", session_branch_bind_from, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    msg = args.extract_plain_text().strip()
    
    context_core = ContextCore(persona_info)
    prompt_core = PromptCore(persona_info)
    config_core = ConfigCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        context_response = await context_core.bind_from(msg)
        prompt_response = await prompt_core.bind_from(msg)
        config_response = await config_core.bind_from(msg)

        await send_msg.send_multiple_responses(
            (context_response, "Context"),
            (prompt_response, "Prompt"),
            (config_response, "Config"),
        )