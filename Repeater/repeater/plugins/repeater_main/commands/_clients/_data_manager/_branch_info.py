from pydantic import BaseModel
from datetime import datetime

class BranchInfo(BaseModel):
    """Branch Info"""
    branch_id: str = ""
    size: int = 0
    modified_time: int = 0
    readable_size: str = ""

    def created_time(self) -> datetime:
        return datetime.fromtimestamp(self.modified_time)