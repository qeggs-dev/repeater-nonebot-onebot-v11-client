from pydantic import BaseModel
from typing import Literal

class UrlFile(BaseModel):
    type: Literal["url"] = "url"
    url: str