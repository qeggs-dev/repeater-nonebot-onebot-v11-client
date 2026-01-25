from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ContextCore, PromptCore, ConfigCore
from ....assist import PersonaInfo, SendMsg

delsession = on_command("delSession", aliases={"ds", "delete_session", "Delete_Session", "DeleteSession"}, rule=to_me(), block=True)

@delsession.handle()
async def handle_delete_session(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Mixed.Delete_Session", delsession, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    context_core = ContextCore(persona_info)
    prompt_core = PromptCore(persona_info)
    config_core = ConfigCore(persona_info)
    response_context = await context_core.delete()
    response_prompt = await prompt_core.delete()
    response_config = await config_core.delete()
    await send_msg.send_multiple_responses(
        (response_context, "Context"),
        (response_prompt, "Prompt"),
        (response_config, "Config")
    )