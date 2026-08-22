from pydantic import BaseModel
from .render_status import RenderStatus
from .details_time import DetailsTime

class RendedImage(BaseModel):
    image_url: str = ""
    file_uuid: str = ""
    style: str = ""
    html_template: str = ""
    status: RenderStatus = RenderStatus.SUCCESS
    browser_used: str = ""
    url_expiry_time: float = 0.0
    error: str | None = None
    text: str = ""
    image_render_time_ms: int = 0
    created: float = 0.0
    created_ms: int = 0
    details_time: DetailsTime | None = None