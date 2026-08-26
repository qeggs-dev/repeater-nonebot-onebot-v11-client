from pydantic import BaseModel
from ....client_configs import HelloContent

class UserConfigs(BaseModel):
    backend: str | None = None
    hello_content: HelloContent | None = None
    variables: dict | None = None