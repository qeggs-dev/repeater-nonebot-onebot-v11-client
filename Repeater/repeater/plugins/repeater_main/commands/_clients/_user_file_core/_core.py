import json
import httpx
from typing import (
    Optional,
    Union
)

from ....core_net_configs import *
from ....assist import PersonaInfo
from ....logger import logger

class UserFileCore:
    def __init__(self, info: PersonaInfo):
        self._info = info
    # region get_utl
    async def get_user_data_file_url(self):
        logger.info("Get user data file url", module = "user_file.core")
        return f"{DOWNLOAD_USER_DATA_FILE_ROUTE}/{self._info.namespace_str}.zip"
    # endregion