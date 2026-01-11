from pydantic import BaseModel

class BranchInfo(BaseModel):
    """Branch Info"""
    branch_id: str = ""
    size: int = 0
    modified_time: int = 0
    readable_size: str = ""