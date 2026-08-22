import asyncio

from nonebot.adapters.onebot.v11 import Bot
from typing import Any, Awaitable, ClassVar
from functools import wraps
from cachetools import TTLCache
from ...client_configs import storage_configs
from ...logger import logger

class CachedAPI(Bot):
    """
    缓存 API

    装饰过的 OneBot v11 Bot 对象
    会缓存 API 的返回值以减少调用次数
    """
    cache: ClassVar[TTLCache[tuple[str, frozenset], Any, float]] = TTLCache( # type: ignore
        maxsize = storage_configs.platform_interface.cache_size,
        ttl = storage_configs.platform_interface.cache_timeout
    )
    cache_lock: ClassVar[asyncio.Lock] = asyncio.Lock()

    @wraps(Bot.call_api)
    async def call_api(self, api: str, **data: Any) -> Any:
        if storage_configs.platform_interface.cache:
            try:
                key: tuple[str, frozenset] = (api, frozenset(data.items()))
                cacheable: bool = True
            except TypeError:
                cacheable = False
            
            async with self.cache_lock:
                if cacheable:
                    if key in self.cache:
                        logger.info(
                            "Cache hit: {name}",
                            name = api
                        )
                        result = self.cache[key]
                        return result
                    else:
                        logger.info(
                            "Cache miss: {name}",
                            name = api
                        )
                else:
                    logger.info(
                        "Is not cacheable call: {name}",
                        name = api
                    )
            
        result = await super().call_api(api, **data)

        if storage_configs.platform_interface.cache:
            async with self.cache_lock:
                if cacheable:
                    self.cache[key] = result
        
        return result