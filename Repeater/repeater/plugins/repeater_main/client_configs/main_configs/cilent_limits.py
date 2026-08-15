from httpx import Limits
from pydantic import BaseModel

class ClientLimits(BaseModel, frozen=True):
    max_connections: int | None = 100
    max_keepalive_connections: int | None = 20
    keepalive_expiry: int | float | None = 5