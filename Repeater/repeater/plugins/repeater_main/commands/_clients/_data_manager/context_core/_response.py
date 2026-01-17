from pydantic import BaseModel, Field

class WithdrawResponse(BaseModel):
    status: str = "success"
    deleted: int = 0
    deleted_context: list[dict] = Field(default_factory=list)
    delete_context_pair: int = 0
    context: list[dict] = Field(default_factory=list)

class ContextTotalLengthResponse(BaseModel):
    total_context_length: int = 0
    context_length: int = 0
    average_content_length: float = 0.0