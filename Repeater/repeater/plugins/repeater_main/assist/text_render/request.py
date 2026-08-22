from pydantic import BaseModel

class RenderRequest(BaseModel):
    text: str
    style: str | None = None
    image_expiry_time: int | None = None
    html_template: str | None = None
    document_bottom_comment: str | None = None
    width: int | None = None
    height: int | None = None
    direct_output: bool | None = None
    no_pre_labels: bool | None = None
    no_escape: bool | None = None
    quality: int | None = None