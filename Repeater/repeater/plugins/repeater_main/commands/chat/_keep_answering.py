from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment

from .._clients import ChatCore, ChatSendMsg
from ...assist import PersonaInfo
from ...logger import logger

keepAnswering = on_command("keepAnswering", aliases={"ka", "keep_answering", "Keep_Answering", "KeepAnswering"}, rule=to_me(), block=True)

@keepAnswering.handle()
async def handle_keep_answering(bot: Bot, event: MessageEvent):
    persona_info = PersonaInfo(bot, event)

    logger.info(
        "Received a message from {namespace}",
        namespace=persona_info.namespace_str,
        module = "Chat.Keep_Answering"
    )

    chat_core = ChatCore(persona_info)

    response = await chat_core.send_message()
    
    send_msg = ChatSendMsg(
        "Keep_Answering",
        persona_info,
        keepAnswering,
        response
    )
    await send_msg.send()