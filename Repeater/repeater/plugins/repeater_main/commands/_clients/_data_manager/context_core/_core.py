import json
import httpx
from typing import (
    Optional,
    Union
)

from .....core_net_configs import *
from .....assist import PersonaInfo, Response
from .....logger import logger as base_logger
from ._response import (
    WithdrawResponse,
    ContextTotalLengthResponse
)
from .._base_user_data_core import UserDataCore

logger = base_logger.bind(module = "Context.Core")

class ContextCore(UserDataCore):
    _httpx_client = httpx.AsyncClient(
        timeout = storage_configs.server_api_timeout.context
    )

    def __init__(self, info: PersonaInfo):
        super().__init__(info, "context")
    
    # region inject context
    async def inject_context(self, text: str, role: str) -> Response[None]:
        logger.info("Injecting {role} context", role = role)
        response = await self._httpx_client.post(
            f"{INJECT_CONTEXT_ROUTE}/{self._info.namespace_str}",
            data={
                "text": text,
                "role": role
            }
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = None
        )
    # endregion
    
    # region withdraw
    async def withdraw(self, context_pair_num: int = 1) -> Response[WithdrawResponse | None]:
        logger.info("Withdrawing context")
        response = await self._httpx_client.post(
            f"{WIHTDRAW_CONTEXT_ROUTE}/{self._info.namespace_str}",
            data={
                "context_pair_num": context_pair_num
            }
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = WithdrawResponse(
                **response.json()
            ) if response.status_code == 200 else None
        )
    # endregion

    # region get context total length
    async def get_context_total_length(self) -> Response[ContextTotalLengthResponse | None]:
        logger.info("Getting context total length")
        response = await self._httpx_client.get(
            f"{GET_CONTEXT_LENGTH_ROUTE}/{self._info.namespace_str}"
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = ContextTotalLengthResponse(
                **response.json()
            ) if response.status_code == 200 else None
        )
    # endregion