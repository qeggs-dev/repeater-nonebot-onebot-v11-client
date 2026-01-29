from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot
from typing import Optional
import asyncio

get_namespace = on_command("getNamespace", aliases={"gns", "get_namespace", "Get_Namespace", "GetNamespace"}, rule=to_me(), block=True)

from ..assist import (
    get_first_mentioned_user,
    PersonaInfo,
    Namespace,
    SendMsg
)

@get_namespace.handle()
async def handle_get_namespace(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)
    send_msg = SendMsg(
        "Namespace.Get_Namespace",
        get_namespace,
        persona_info
    )
    
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        mentioned_id = get_first_mentioned_user(event)
        group_id = persona_info.group_id
        namespace = persona_info.namespace
        if mentioned_id is None:
            await send_msg.send_prompt(namespace.namespace)
        else:
            await send_msg.send_prompt(
                Namespace(
                    mode = namespace.mode,
                    group_id = group_id,
                    user_id = mentioned_id
                ).namespace
            )
