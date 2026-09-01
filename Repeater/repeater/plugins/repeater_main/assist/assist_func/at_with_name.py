from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.adapters import Bot
from cachetools import LRUCache

user_cache = LRUCache(maxsize=1000)

async def at_with_name(bot: Bot, event: MessageEvent) -> Message:
    """
    处理@消息，将@的ID替换为昵称

    :param bot: Bot对象
    :param event: MessageEvent对象
    """
    new_msg = Message()
    
    for seg in event.message:
        if seg.type == "at":
            qq = seg.data.get("qq", "")
            if qq in user_cache:  # 优先读缓存
                name = user_cache[qq]
            else:
                try:
                    info = await bot.get_stranger_info(user_id=int(qq))
                    name = info["nickname"]
                    user_cache[qq] = name  # 存入缓存
                except:
                    name = qq  # 失败则用 QQ 号代替
            new_msg.append(f"@{name}")
        else:
            new_msg.append(seg)
    
    return new_msg