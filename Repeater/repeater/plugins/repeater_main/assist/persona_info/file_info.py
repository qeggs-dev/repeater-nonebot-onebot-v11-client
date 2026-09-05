from pydantic import BaseModel, ConfigDict

class FileInfo(BaseModel):
    """
    文件信息
    """
    model_config = ConfigDict(
        extra = "ignore",
        frozen = True
    )

    name: str
    size: int
    id: str
    url: str