from nonebot import on_message
from nonebot.internal.matcher.matcher import Matcher
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from ...logger import logger

from .._clients import ChatCore, ChatSendMsg
from ...assist import PersonaInfo, SendMsg, MessageSource

smart_at: type[Matcher] = on_message(rule=to_me(), priority=100, block=True)

@smart_at.handle()
async def handle_smart_at(bot: Bot, event: MessageEvent):
    persona_info = PersonaInfo(bot, event)
    sendmsg = SendMsg("Chat.Smart_at", smart_at, persona_info)

    logger.info(
        "Received a message {message} from {namespace}",
        message = persona_info.message_str,
        namespace = persona_info.namespace_str,
        module = "Chat.Smart_at"
    )

    message = persona_info.message
    
    if not persona_info:
        if persona_info.source == MessageSource.GROUP:
            await sendmsg.send_hello()
        else:
            return
    
    core = ChatCore(persona_info)

    images: list[str] = await persona_info.get_images_url()

    
    response = await core.send_message(
        message = message.extract_plain_text().strip(),
        image_url = images
    )
    
    chat_send_msg = ChatSendMsg(
        "Chat.Smart_at",
        persona_info,
        smart_at,
        response
    )
    await chat_send_msg.send()