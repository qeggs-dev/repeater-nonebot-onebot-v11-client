from pydantic import BaseModel
from typing import Literal


class Base64File(BaseModel):
    type: Literal["base64"] = "base64"
    data: str