import random
import asyncio
from typing import Any
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent, MessageSegment
from nonebot.params import (
    CommandArg,
    ArgPlainText,
    Arg
)
from ...assist import PersonaInfo, MessageSource, SendMsg

choose_group_member = on_command("chooseGroupMember", aliases={"cgm","choose_group_member", "Choose_Group_Member", "ChooseGroupMember"}, rule=to_me(), block=True)

def generate_text(choiced: list[dict[str, Any]]):
    text_buffer: list[str] = []
    for index, member in enumerate(choiced, start = 1):
        nickname = member.get("card")
        if not nickname:
            nickname = member.get("nickname")
        text_buffer.append(f"{index}. {nickname}")
    text = "\n".join(text_buffer)
    return text

@choose_group_member.handle()
async def choose_group_member_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)
    send_msg = SendMsg("More.Choose_Group_Member", choose_group_member, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    
    if persona_info.source == MessageSource.PRIVATE:
        await send_msg.send_error("The current feature cannot be used in private chat.")
    
    group_id = persona_info.group_id
    
    try:
        n = int(args.extract_plain_text())
    except (ValueError, TypeError):
        await send_msg.send_error("Please enter a number.")
    if n > 0:
        text = ""
        member_list = await bot.get_group_member_list(
            group_id = group_id,
            no_cache = False
        )
        if n > len(member_list):
            await send_msg.send_error(f"The current number is too large, please enter a number less than {len(member_list)}.")
        choiced: list[dict[str, Any]] = random.sample(member_list, n)
        text = await asyncio.to_thread(generate_text, choiced)
        if n > 10:
            await send_msg.send_mixed_render(
                text,
                prompt_mode = True
            )
        else:
            await send_msg.send_prompt(text)
    else:
        await send_msg.send_error("The input must be a positive integer!")