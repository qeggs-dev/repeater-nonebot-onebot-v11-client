from dataclasses import dataclass
from enum import Enum
from ..core_net_configs import storage_configs

class MessageSource(Enum):
    """
    消息来源
    """
    GROUP = "group"
    PRIVATE = "private"

@dataclass
class Namespace:
    """
    用户命名空间
    """
    mode: MessageSource = MessageSource.GROUP
    group_id: int | None = None
    user_id: int = 0

    @property
    def namespace(self) -> str:
        if self.mode == MessageSource.GROUP:
            if self.group_id is None:
                raise ValueError("group_id cannot be None when mode is GROUP")
            if storage_configs.merge_group_id:
                return f"Group_{self.group_id}"
            else:
                return f"Group_{self.group_id}_{self.user_id}"
        else:
            return f"Private_{self.user_id}"
    
    @property
    def public_space_id(self):
        if self.mode == MessageSource.GROUP:
            if self.group_id is None:
                raise ValueError("group_id cannot be None when mode is GROUP")
            return f"Group_{self.group_id}_Public_Space"
        else:
            return f"Private_{self.user_id}_Public_Space"
    
    def __str__(self) -> str:
        return self.namespace