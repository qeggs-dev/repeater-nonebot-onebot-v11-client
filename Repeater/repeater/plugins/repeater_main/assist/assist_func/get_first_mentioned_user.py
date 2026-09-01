from nonebot.adapters.onebot.v11 import MessageEvent
from typing import Optional

user_cache = {}  # 缓存用户昵称

def get_first_mentioned_user(event: MessageEvent) -> Optional[str]:
    """
    获取消息中第一个@的 ID

    :param event: 消息事件对象
    """
    # 获取机器人自己的 ID
    bot_id = str(event.self_id)
    
    # 遍历消息中的所有@消息段
    for segment in event.message:
        if segment.type == "at":
            mentioned_id = segment.data["qq"]
            # 检查是否@的是非机器人用户
            if mentioned_id != bot_id:
                return mentioned_id
    return None