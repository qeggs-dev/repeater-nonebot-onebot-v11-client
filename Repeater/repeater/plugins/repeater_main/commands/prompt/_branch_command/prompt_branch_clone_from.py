from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ..._clients import PromptCore
from ....assist import PersonaInfo, SendMsg

prompt_branch_clone_from = on_command("promptBranchCloneFrom", aliases={"pbcf", "prompt_branch_clone_from", "Prompt_Branch_Clone_From", "PromptBranchCloneFrom"}, rule=to_me(), block=True)

@prompt_branch_clone_from.handle()
async def handle_prompt_branch_clone_from(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Prompt.Prompt_Branch_Clone_From", prompt_branch_clone_from, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    msg = args.extract_plain_text().strip()
    
    prompt_core = PromptCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await prompt_core.clone_from(msg)
        await send_msg.send_response_check_code(response, f"Clone Prompt Branch from {msg}")