from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from ...logger import logger

async def get_message_event(bot: Bot, message_id: int) -> MessageEvent:
    response = await bot.get_msg(
        message_id = message_id
    )
    # 兼容 MessageEvent

    if "post_type" not in response:
        response["post_type"] = "message"
    elif response["post_type"] != "message":
        logger.warning(
            "get_message_event: post_type is {post_type}",
            post_type = response["post_type"]
        )
        response["post_type"] = "message"

    if "self_id" not in response:
        response["self_id"] = bot.self_id
    
    return MessageEvent(**response)