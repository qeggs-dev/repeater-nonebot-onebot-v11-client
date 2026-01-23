from ..core_net_configs import *
from pydantic import BaseModel
from ._response import Response
from ._namespace import Namespace
import httpx

class RendedImage(BaseModel):
    image_url: str = ""
    file_uuid: str = ""
    style: str = ""
    timeout: float = 0.0
    text: str = ""
    created: float = 0.0
    created_ms: int = 0

class TextRender:
    _client = httpx.AsyncClient()

    def __init__(self, namespace: str | Namespace, timeout:float = 60.0):
        self.url = f"{BACKEND_HOST}:{BACKEND_PORT}"
        if isinstance(namespace, str):
            self.namespce = namespace
        elif isinstance(namespace, Namespace):
            self.namespce = namespace.namespace
        else:
            raise TypeError(f"namespace must be str or Namespace, not {type(namespace)}")
        self._timeout = timeout

    async def render(self, text: str) -> Response[RendedImage]:
        response = await self._client.post(
            f"{TEXT_RENDER_ROUTE}/{self.namespce}",
            json={"text": text},
            timeout = self._timeout
        )
        try:
            response_json:dict = response.json()
        except:
            response_json = {}
        
        return Response(
            code=response.status_code,
            text=response.text,
            data=RendedImage(**response_json),
        )
        