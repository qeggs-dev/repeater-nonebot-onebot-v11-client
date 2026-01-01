import json
import httpx
from typing import (
    Optional,
    Union
)

from ....core_net_configs import *
from ....assist import Response, PersonaInfo
from ....logger import logger as base_logger

logger = base_logger.bind(module = "Prompt.Core")

class PromptCore:
    _httpx_client = httpx.AsyncClient(
        timeout = storage_configs.server_api_timeout.prompt
    )

    def __init__(self, info: PersonaInfo):
        self._info = info
    
    # region set prompt  
    async def set_prompt(self, prompt: str) -> Response[None]:
        logger.info("Setting prompt")
        response = await self._httpx_client.put(
            f"{SET_PROMPT_ROUTE}/{self._info.namespace_str}",
            data={
                "prompt": prompt
            }
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = None
        )
    # endregion
    
    # region delete
    async def delete_prompt(self) -> Response[None]:
        logger.info("Deleting prompt")
        response = await self._httpx_client.delete(
            f"{DELETE_PROMPT_ROUTE}/{self._info.namespace_str}"
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = None
        )
    
    async def delete_subprompt(self) -> Response[None]:
        logger.info("Deleting subprompt")
        response = await self._httpx_client.delete(
            f"{DELETE_SUBSESSION_PROMPT_ROUTE}",
            params={"session_id": self._info.namespace_str}
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = None
        )
    # endregion

    # region change subsession
    async def change_prompt_branch(self, new_branch_id: str) -> Response[None]:
        logger.info("Changing prompt branch")
        response = await self._httpx_client.put(
            f"{CHANGE_PROMPT_BRANCH_ROUTE}/{self._info.namespace_str}",
            data={
                "new_branch_id": new_branch_id
            }
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = None
        )
    # endregion