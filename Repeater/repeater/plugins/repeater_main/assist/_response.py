from typing import Generic, TypeVar, Type, Any
from httpx import Response as HTTPXResponse
from ._error_response import ErrorResponse
from pydantic import BaseModel

T_Response = TypeVar("T_Response")

class Response(Generic[T_Response]):
    def __init__(
            self,
            httpx_response: HTTPXResponse,
            model: Type[T_Response] | None = None
        ):
        self._httpx_response = httpx_response
        self._model = model
    
    @property
    def code(self) -> int:
        return self._httpx_response.status_code

    @property
    def text(self) -> str:
        return self._httpx_response.text
    
    @property
    def content(self) -> bytes:
        return self._httpx_response.content
    
    def json(self) -> Any:
        return self._httpx_response.json()
    
    def get_data(self) -> T_Response | None:
        if issubclass(self._model, BaseModel):
            data: Any = self.json()
            return self._model(**data)
    
    def get_error(self) -> ErrorResponse | None:
        if self.code != 200:
            return ErrorResponse(**self.json())

    def __bool__(self) -> bool:
        return self.code == 200