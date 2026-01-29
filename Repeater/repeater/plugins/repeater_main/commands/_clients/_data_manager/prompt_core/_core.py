import json
import httpx
from typing import (
    Optional,
    Union
)

from .....core_net_configs import *
from .....assist import Response, PersonaInfo
from .....logger import logger as base_logger
from .._base_user_data_core import UserDataCore

logger = base_logger.bind(module = "Prompt.Core")

class PromptCore(UserDataCore):
    _httpx_client = httpx.AsyncClient(
        timeout = storage_configs.server_api_timeout.prompt
    )

    def __init__(self, info: PersonaInfo):
        super().__init__(info, "prompt")
    
    # region set prompt  
    async def set_prompt(self, prompt: str) -> Response[None]:
        logger.info("Setting prompt")
        response = await self._httpx_client.put(
            f"{SET_PROMPT_ROUTE}/{self._info.namespace_str}",
            data={
                "prompt": prompt
            }
        )
        return Response(response)
    # endregion