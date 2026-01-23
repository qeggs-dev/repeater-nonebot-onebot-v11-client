from typing import Generic, TypeVar, Type, Any
from httpx import Response as HTTPXResponse
from pydantic import BaseModel

T_Response = TypeVar("T_Response")

class Response(Generic[T_Response]):
    def __init__(
            self,
            httpx_response: HTTPXResponse,
            model: Type[T_Response] | None = None
        ):
        self._code: int = httpx_response.status_code
        self._text: str = httpx_response.text
        self._content: bytes = httpx_response.content
        
        if issubclass(model, BaseModel):
            try:
                data: Any = httpx_response.json()
            except Exception:
                self._data: None = None
            
            try:
                self._data: T_Response = model(**data)
            except Exception:
                self._data: None = None
    
    @property
    def code(self) -> int:
        return self._code

    @property
    def text(self) -> str:
        return self._text
    
    @property
    def content(self) -> bytes:
        return self._content

    @property
    def data(self) -> T_Response | None:
        return self._data

    def __bool__(self) -> bool:
        return self.code == 200