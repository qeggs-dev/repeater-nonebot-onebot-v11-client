from pydantic import BaseModel


class PermissionRule(BaseModel):
    """
    权限规则
    """
    group_id: str | None = None
    user_id: str | None = None