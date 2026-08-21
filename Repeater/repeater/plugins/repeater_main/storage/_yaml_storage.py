import os
from ._sync_base_storage import TextStorage
from pathlib import Path
from typing import Any, TypeVar
import yaml
from ..logger import logger as base_logger

logger = base_logger.bind(module = "Storage.Sync.Yaml")

T = TypeVar("T")

class YamlStorage(TextStorage):
    """
    YAML Storage

    存储文件格式为 YAML
    """
    def load_yaml(self, path: str | os.PathLike, default: T = None) -> Any | T:
        try:
            logger.info(f"Loading yaml from {path}")
            return self.load(
                path
            )
        except Exception as e:
            logger.error(f"load yaml error: {e}")
            return default
    
    def save_yaml(self, path: str | os.PathLike, data: Any):
        try:
            logger.info(f"Saving yaml to {path}")
            self.save(
                path,
                yaml.safe_dump(data)
            )
        except Exception as e:
            logger.error(f"save yaml error: {e}")
