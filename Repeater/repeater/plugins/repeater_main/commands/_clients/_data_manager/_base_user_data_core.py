import json
import httpx
from abc import ABC

from ....core_net_configs import *
from ....assist import Response, PersonaInfo
from ....logger import logger as base_logger
from ._branch_info import BranchInfo

logger = base_logger.bind(module = "UserData.Core")

class UserDataCore(ABC):
    _httpx_client = httpx.AsyncClient()

    def __init__(self, info: PersonaInfo, branch_id: str):
        self._info = info
        self._branch_id = branch_id

    # region change subsession
    async def change_branch(self, new_branch_id: str) -> Response[None]:
        response = await self._httpx_client.put(
            f"{BASE_URL}/userdata/{self._branch_id}/change/{self._info.namespace_str}",
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

    # region Delete
    async def delete(self) -> Response[None]:
        response = await self._httpx_client.delete(
            f"{BASE_URL}/userdata/{self._branch_id}/delete/{self._info.namespace_str}"
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = None
        )
    # endregion

    # region clone
    async def clone(self, dst_branch_id: str) -> Response[None]:
        response = await self._httpx_client.post(
            f"{BASE_URL}/userdata/{self._branch_id}/clone/{self._info.namespace_str}",
            data={
                "dst_branch_id": dst_branch_id
            }
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = None
        )
    # endregion

    # region clone from
    async def clone_from(self, src_branch_id: str) -> Response[None]:
        response = await self._httpx_client.post(
            f"{BASE_URL}/userdata/{self._branch_id}/clone_from/{self._info.namespace_str}",
            data={
                "src_branch_id": src_branch_id
            }
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = None
        )
    # endregion

    # region bind
    async def bind(self, dst_branch_id: str) -> Response[None]:
        response = await self._httpx_client.post(
            f"{BASE_URL}/userdata/{self._branch_id}/bind/{self._info.namespace_str}",
            data={
                "dst_branch_id": dst_branch_id
            }
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = None
        )
    # endregion

    # region bind from
    async def bind_from(self, src_branch_id: str) -> Response[None]:
        response = await self._httpx_client.post(
            f"{BASE_URL}/userdata/{self._branch_id}/bind_from/{self._info.namespace_str}",
            data={
                "src_branch_id": src_branch_id
            }
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = None
        )
    # endregion

    async def branch_info(self) -> Response[BranchInfo]:
        response = await self._httpx_client.get(
            f"{BASE_URL}/userdata/{self._branch_id}"
        )
        try:
            data = response.json()
            data = BranchInfo(**data)
        except Exception as e:
            logger.exception(e)
            data = None
        
        return Response(
            code = response.status_code,
            text = response.text,
            data = data
        )

    # region close
    def close(self) -> None:
        self._httpx_client.aclose()
    # endregion