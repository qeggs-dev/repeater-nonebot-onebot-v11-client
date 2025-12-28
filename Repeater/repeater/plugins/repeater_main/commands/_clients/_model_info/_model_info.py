from pydantic import BaseModel, Field
from ._model_types import ModelType

class ModelInfo(BaseModel):
    name: str = ""
    url: str = ""
    id: str = ""
    parent: str = ""
    uid: str = ""
    type: ModelType = ModelType.CHAT
    timeout: float = 600.0