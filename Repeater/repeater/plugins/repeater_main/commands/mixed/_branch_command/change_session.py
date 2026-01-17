from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ContextCore, PromptCore, ConfigCore
from ....assist import PersonaInfo, SendMsg

change_session = on_command("changeSession", aliases={"cs", "change_session", "Change_Session", "ChangeSession"}, rule=to_me(), block=True)

@change_session.handle()
async def handle_change_session(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Mixed.Change_Session", change_session, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    context_core = ContextCore(persona_info)
    prompt_core = PromptCore(persona_info)
    config_core = ConfigCore(persona_info)
    response_context = await context_core.change_branch(
        persona_info.message_str
    )
    response_prompt = await prompt_core.change_branch(
        persona_info.message_str
    )
    response_config = await config_core.change_branch(
        persona_info.message_str
    )
    await send_msg.send_multiple_responses(
        (response_context, "Context"),
        (response_prompt, "Prompt"),
        (response_config, "Config")
    )