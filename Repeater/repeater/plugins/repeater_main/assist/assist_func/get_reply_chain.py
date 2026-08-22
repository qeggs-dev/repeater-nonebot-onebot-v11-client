from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent
from ...logger import logger
from typing import AsyncGenerator
from ...client_configs import storage_configs
from .get_reply_msgs import get_reply_msgs

async def get_reply_chain(
    bot: Bot,
    message: Message,
) -> AsyncGenerator[MessageEvent, None]:
    """
    获取回复链

    注：解析时，它会默认消息段中只有一个 reply 消息段，
    如果有存在多个，则使用第一个

    :param bot: Bot
    :param message: 消息
    """
    times: int = 0
    while True:
        if times > storage_configs.max_reply_chain_length:
            break
        reply_messages = await get_reply_msgs(
            bot = bot,
            message = message
        )
        if len(reply_messages) >= 1:
            event = reply_messages[0]
            yield event
            message = event.message
        else:
            break
        times += 1