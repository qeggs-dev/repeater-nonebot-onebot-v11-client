import httpx
from ....logger import logger as base_logger
from typing import (
    Optional,
    Union,
    Any,
)

from ....core_net_configs import *
from ....assist import Response, PersonaInfo
from ....exit_register import ExitRegister
from ._model_types import ModelType
from ._model_info import ModelInfo

exit_register = ExitRegister()
logger = base_logger.bind(module = "Config.Core")

class ModelInfoCore:
    def __init__(self):
        self._client = httpx.AsyncClient(
            timeout = storage_configs.server_api_timeout.config
        )

    
    # region get model list
    async def get_model_list(self, type: ModelType) -> Response[list[str] | None]:
        response = await self._client.get(
            f"{GET_MODEL_UID_LIST}/{type.value}",
        )
        return Response(
            response
        )
    # endregion

    # region get model info
    async def get_model_info(self, type: ModelType, uid: str) -> Response[ModelInfo]:
        response = await self._client.get(
            f"{GET_MODEL_INFO}/{type.value}/{uid}",
        )
        return Response(
            response,
            model = ModelInfo
        )

    # region close
    def close(self) -> None:
        self._client.aclose()
    # endregion