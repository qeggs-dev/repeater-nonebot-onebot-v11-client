import json
import httpx
from typing import (
    Optional,
    Union
)

from ....core_net_configs import *
from ....assist import Response
from .version_model import VersionModel

class VersionAPICore:
    _httpx_client = httpx.AsyncClient(
        timeout = storage_configs.server_api_timeout.variable_expansion
    )

    async def get_version(self) -> Response[VersionModel]:
        response = await self._httpx_client.get(
            url = VERSION_ROUTE,
        )
        return Response(
            httpx_response = response,
            model = VersionModel
        )