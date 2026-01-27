from pydantic import BaseModel

class VersionModel(BaseModel):
    """
    Model for version command
    """
    core: str = "0.0.0.0"
    api: str = "0.0.0.0"