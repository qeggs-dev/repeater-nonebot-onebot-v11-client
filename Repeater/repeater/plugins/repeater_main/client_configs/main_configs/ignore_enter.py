from pydantic import BaseModel, Field

class IgnoreEnter(BaseModel):
    group_ignore_enter_set: set[str] = Field(default_factory=set)
    user_ignore_enter_set: set[str] = Field(default_factory=set)
    unignore_enter_commands: set[str] = Field(default_factory=set)
    allow_check_online: bool = True
        
    def ignore_enter_check(self, group_id: str | None, user_id: str) -> bool:
        if group_id in self.group_ignore_enter_set or user_id in self.user_ignore_enter_set:
            return True
        else:
            return False