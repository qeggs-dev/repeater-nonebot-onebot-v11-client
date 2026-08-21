from pydantic import BaseModel
from typing import Any

class SendMessage(BaseModel):
    text: str | None = None
    suffix: str | None = None
    images: list[str] | None = None
    audios: list[str] | None = None
    videos: list[str] | None = None
    files: list[str] | None = None
    extra: dict[str, Any] | None = None