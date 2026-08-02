from pydantic import BaseModel
from typing import Literal

class PathFile(BaseModel):
    type: Literal["path"] = "path"
    path: str