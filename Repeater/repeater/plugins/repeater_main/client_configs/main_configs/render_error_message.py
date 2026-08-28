from pydantic import BaseModel

class RenderErrorMessage(BaseModel):
    style: str | None = None
    html_template: str | None = None
    title: str | None = None