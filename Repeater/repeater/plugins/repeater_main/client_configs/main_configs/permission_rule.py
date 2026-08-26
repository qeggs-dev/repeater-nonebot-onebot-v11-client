from pydantic import BaseModel


class PermissionRule(BaseModel):
    """
    权限规则
    """
    super_group: str | None = None
    super_user: str | None = None