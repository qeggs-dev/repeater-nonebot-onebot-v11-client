from enum import StrEnum

class RenderStatus(StrEnum):
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"