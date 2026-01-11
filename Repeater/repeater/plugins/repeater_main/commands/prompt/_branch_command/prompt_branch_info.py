from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ..._clients import PromptCore
from ....assist import PersonaInfo, SendMsg

prompt_branch_info = on_command("promptBranchInfo", aliases={"pbi", "prompt_branch_info", "Prompt_Branch_Info", "PromptBranchInfo"}, rule=to_me(), block=True)

@prompt_branch_info.handle()
async def handle_prompt_branch_info(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Prompt.Prompt_Branch_Info", prompt_branch_info, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    
    prompt_core = PromptCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await prompt_core.branch_info()
        if response.code == 200:
            await send_msg.send_prompt(
                f"Branch Type: Prompt\n"
                f"Branch ID: {response.data.branch_id}\n"
                f"Branch Size: {response.data.size}\n"
                f"Branch Readable Size: {response.data.readable_size}\n"
                f"Branch Create Time: {response.data.created_time().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
        else:
            await send_msg.send_response(response, "Get Prompt branch info failed")