from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .._clients import PromptCore
from ...assist import PersonaInfo, SendMsg

delprompt = on_command("deletePrompt", aliases={"dp", "delete_prompt", "Delete_Prompt", "DeletePrompt"}, rule=to_me(), block=True)

@delprompt.handle()
async def handle_delete_prompt(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)
    send_msg = SendMsg("Prompt.Delete_Prompt", delprompt, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    
    prompt_core = PromptCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await prompt_core.delete_prompt()
        await send_msg.send_response(response, f"Delete Prompt from {persona_info.namespace_str}")
