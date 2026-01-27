import httpx

from ....core_net_configs import *
from ....assist import Response

class LicenseCore:
    _httpx_client = httpx.AsyncClient(
        base_url = BASE_URL,
        timeout = storage_configs.server_api_timeout.variable_expansion
    )

    async def get_requirement_license(self, requirement_name: str) -> Response[dict[str, str]]:
        response = await self._httpx_client.get(
            url = f"/license/requirement/{requirement_name}",
        )
        return Response(
            httpx_response = response,
            data = response.json()
        )

    async def get_requirement_list(self) -> Response[list[str]]:
        response = await self._httpx_client.get(
            url = f"/license/requirement_list",
        )
        return Response(
            httpx_response = response,
            data = response.json()
        )
    
    async def get_server_licenses(self) -> Response[dict[str, str]]:
        response = await self._httpx_client.get(
            url = "/license/self",
        )
        return Response(
            httpx_response = response,
            data = response.json()
        )