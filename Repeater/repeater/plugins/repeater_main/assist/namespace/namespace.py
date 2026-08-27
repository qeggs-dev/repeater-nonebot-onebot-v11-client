import re
import hashlib
from pydantic import BaseModel, ConfigDict
from ...client_configs import storage_configs
from .message_source import MessageSource

group_pattern = re.compile(r"^Group_(?P<group_id>[0-9]+)_(?P<user_id>[0-9]+)$")
private_pattern = re.compile(r"^Private_(?P<user_id>[0-9]+)$")

class Namespace(BaseModel):
    """
    用户命名空间
    """
    model_config = ConfigDict(
        validate_assignment=True,
        frozen = True
    )

    mode: MessageSource = MessageSource.GROUP
    group_id: str | None = None
    user_id: str = ""

    @classmethod
    def from_str(cls, string: str) -> "Namespace":
        match_result = group_pattern.match(string)
        if match_result is not None:
            return cls(
                mode = MessageSource.GROUP,
                group_id = match_result.group("group_id"),
                user_id = match_result.group("user_id")
            )

        match_result = private_pattern.match(string)
        if match_result is not None:
            return cls(
                mode = MessageSource.PRIVATE,
                user_id = match_result.group("user_id")
            )

        raise ValueError(f"Invalid namespace string: {string}")

    @property
    def _namespace(self) -> str:
        if self.mode == MessageSource.GROUP:
            return f"Group_{self.group_id}_{self.user_id}"
        elif self.mode == MessageSource.PRIVATE:
            return f"Private_{self.user_id}"
        else:
            return f"UnknownSource_{self.user_id}"
    
    @property
    def namespace_str(self):
        if storage_configs.hash_user_id:
            return hashlib.sha3_256(
                self._namespace.encode("utf-8")
            ).hexdigest()
        else:
            return self._namespace
    
    @property
    def _merge_group_id(self):
        if self.mode == MessageSource.GROUP:
            if self.group_id is None:
                raise ValueError("group_id cannot be None when mode is GROUP")
            return f"Group_{self.group_id}"
        elif self.mode == MessageSource.PRIVATE:
            return f"Private_{self.user_id}"
        else:
            return f"UnknownSource_{self.user_id}"
    
    @property
    def merge_namespace(self):
        if storage_configs.hash_user_id:
            return hashlib.sha3_256(
                self._merge_group_id.encode("utf-8")
            ).hexdigest()
        else:
            return self._merge_group_id
    
    @property
    def _public_space_id(self):
        if self.mode == MessageSource.GROUP:
            if self.group_id is None:
                raise ValueError("group_id cannot be None when mode is GROUP")
            return f"Group_{self.group_id}_Public_Space"
        elif self.mode == MessageSource.PRIVATE:
            return f"Private_{self.user_id}_Public_Space"
        else:
            return f"UnknownSource_{self.user_id}_Public_Space"
    
    @property
    def public_space_id(self):
        if storage_configs.hash_user_id:
            return hashlib.sha3_256(
                self._public_space_id.encode("utf-8")
            ).hexdigest()
        else:
            return self._public_space_id
    
    def __str__(self) -> str:
        return self.namespace_str