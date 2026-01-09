import random
from typing import Any
from pydantic import ValidationError
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from nonebot.params import (
    CommandArg,
    ArgPlainText,
    Arg
)
from ...assist import PersonaInfo, MessageSource, SendMsg

recent_speaking_ranking = on_command("recentSpeakingRanking", aliases={"rsr","recent_speaking_ranking", "Recent_Speaking_Ranking", "RecentSpeakingRanking"}, rule=to_me(), block=True)

@recent_speaking_ranking.handle()
async def recent_speaking_ranking_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)
    send_msg = SendMsg("More.Recent_Speaking_Ranking", recent_speaking_ranking, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    
    if persona_info.source == MessageSource.PRIVATE:
        await send_msg.send_error("The current feature cannot be used in private chat.")
    
    group_id = persona_info.group_id
    
    try:
        n = int(args.extract_plain_text())
    except (ValueError, TypeError):
        await send_msg.send_error("Please enter a valid number.")
    if n > 0:
        text = ""
        message_list = await bot.get_group_msg_history(
            group_id = group_id,
            count = n
        )
        member_speech_count: dict[str, int] = {}
        validation_failure_counter: int = 0
        total_effective: int = 0
        for message in message_list["messages"]:
            try:
                event = MessageEvent(**message)
                member_name = event.sender.card or event.sender.nickname
                total_effective += 1
            except ValidationError:
                try:
                    member_name = message["sender"]["card"] or message["sender"]["nickname"]
                    total_effective += 1
                except KeyError:
                    validation_failure_counter += 1
                    continue
            if member_name not in member_speech_count:
                member_speech_count[member_name] = 1
            else:
                member_speech_count[member_name] += 1
        
        member_speech_count_list = list(member_speech_count.items())
        sorted_member_speech_count_list = sorted(member_speech_count_list, key=lambda x: x[1], reverse=True)

        text_list: list[str] = []
        for index, (name, speech_count) in enumerate(sorted_member_speech_count_list, start = 1):
            text_list.append(f"{index}. {name}: {speech_count}({speech_count / total_effective:.2%})")
        text = "\n".join(text_list)

        if validation_failure_counter > 0:
            await send_msg.send_warning(f"Warning: There are {validation_failure_counter} message verification failures.\n")
        line_count = text.count("\n") + 1
        
        if line_count > 10:
            await send_msg.send_mixed_render(
                text,
                prompt_mode = True,
            )
        else:
            await send_msg.send_prompt(text)
    else:
        await send_msg.send_error("The input must be a positive integer!")