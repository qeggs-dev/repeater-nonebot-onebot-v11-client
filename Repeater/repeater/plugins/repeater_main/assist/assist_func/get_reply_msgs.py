from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message
from ...logger import logger

async def get_reply_msgs(bot: Bot, message: Message) -> list[MessageEvent]:
    msgs: list[MessageEvent] = []
    for msg in message:
        if msg.type == "reply":
            reply_msg = await bot.get_msg(message_id=msg.data["id"])

            # 兼容 MessageEvent
            reply_msg["post_type"] = "message"
            msgs.append(
                MessageEvent(**reply_msg)
            )
    return msgs