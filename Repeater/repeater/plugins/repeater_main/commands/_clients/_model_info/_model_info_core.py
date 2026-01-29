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
    async def get_model_list(self, type: ModelType) -> Response[list[ModelInfo]]:
        response = await self._client.get(
            f"{GET_MODEL_UID_LIST}/{type.value}",
        )
        json_data = response.json()
        if not isinstance(json_data, list):
            return Response(
                response,
                parsed_data = None,
            )
        model_list: list[ModelInfo] = []
        for model_info in json_data:
            model_list.append(
                ModelInfo(**model_info)
            )
        return Response(
            httpx_response = response,
            parsed_data = model_list,
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