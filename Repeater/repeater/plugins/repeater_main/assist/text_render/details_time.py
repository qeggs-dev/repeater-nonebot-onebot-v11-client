from pydantic import BaseModel

class DetailsTime(BaseModel):
    preprocess: int | None = None
    markdown_to_html: int | None = None
    render: int | None = None