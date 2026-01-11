import httpx
from ....logger import logger as base_logger
from typing import (
    Optional,
    Union,
    Any,
)

from ....assist import Response, PersonaInfo
# 服务端配置
from ....core_net_configs import *
from ....exit_register import ExitRegister

exit_register = ExitRegister()
logger = base_logger.bind(module = "Config.Core")

class ConfigCore:
    _httpx_client = httpx.AsyncClient(
        timeout = storage_configs.server_api_timeout.config
    )

    def __init__(self, info: PersonaInfo):
        self._info = info
    
    # region set config
    async def set_config(self, config_key: str, value: Any, item_type: str = "auto") -> Response[Any | None]:
        TYPES = {
            int: "int",
            float: "float",
            str: "string",
            bool: "boolean",
            dict: "dict",
            list: "list",
            None: "null"
        }
        if item_type == "raw":
            item_type = "raw"
        if item_type == "auto":
            if type(value) not in TYPES:
                raise TypeError(f"Unsupported type: {type(value).__name__}")
            item_type = TYPES[type(value)]
        else:
            if item_type not in TYPES:
                raise TypeError(f"Unsupported type: {item_type}")
        logger.info(
            "Set config: {config_key} = {value}(type:{item_type})",
            config_key=config_key,
            value=value,
            item_type=item_type
        )
        response = await self._httpx_client.put(
            f"{SET_CONFIG_ROUTE}/{self._info.namespace_str}/{config_key}",
            json={
                "type": item_type,
                "value": value
            }
        )
        try:
            data = response.json()
        except Exception as e:
            logger.error(f"Error: {e}")
            data = None
        return Response(
            code = response.status_code,
            text = response.text,
            data = data
        )
    # endregion

    # region change config
    async def change_config_branch(self, branch_id: str) -> Response[None]:
        logger.info("Change config: {branch_id}", branch_id=branch_id)
        response = await self._httpx_client.put(
            url = f"{CHANGE_CONFIG_BRANCH_ROUTE}/{self._info.namespace_str}",
            data = {
                "new_branch_id": branch_id
            }
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = None
        )
    # endregion


    # region get config
    async def get_config(self) -> Response[Any | None]:
        logger.info("Get {user} configs", user=self._info.namespace_str)
        response = await self._httpx_client.get(
            f"{GET_CONFIG_ROUTE}/{self._info.namespace_str}"
        )
        try:
            data = response.json()
        except Exception as e:
            logger.error(f"Error: {e}")
            data = None
        return Response(
            code = response.status_code,
            text = response.text,
            data = data
        )
    # endregion

    # region remove config key
    async def remove_config_key(self, config_key: str) -> Response[None]:
        logger.info("Remove config key: {config_key}", config_key=config_key)
        response = await self._httpx_client.delete(
            f"{REMOVE_CONFIG_KEY_ROUTE}/{self._info.namespace_str}/{config_key}"
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = None
        )
    # endregion

    # region delete
    async def delete_config(self) -> Response[None]:
        logger.info("Delete config")
        response = await self._httpx_client.delete(
            f"{DELETE_CONFIG_ROUTE}/{self._info.namespace_str}"
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = None
        )
    # endregion

    # region close
    def close(self) -> None:
        self._httpx_client.aclose()
    # endregion