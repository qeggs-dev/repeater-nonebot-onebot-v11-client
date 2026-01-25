from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ..._clients import PromptCore
from ....assist import PersonaInfo, SendMsg

prompt_branch_bind_from = on_command("promptBranchBindFrom", aliases={"pbbf", "prompt_branch_bind_from", "Prompt_Branch_Bind_From", "PromptBranchBindFrom"}, rule=to_me(), block=True)

@prompt_branch_bind_from.handle()
async def handle_prompt_branch_bind_from(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Prompt.Prompt_Branch_Bind_From", prompt_branch_bind_from, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    msg = args.extract_plain_text().strip()
    
    prompt_core = PromptCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await prompt_core.bind_from(msg)
        await send_msg.send_response(response, f"Bind Prompt Branch from {msg}")