from ..response import Response

class TextRenderException(Exception):
    """Base class for exceptions in text_render module."""
    pass

class RenderResponseException(TextRenderException):
    """Exception raised for errors in the render response."""
    def __init__(self, response: Response):
        self.response = response
        super().__init__(self.response.text)


class InvalidResponseData(TextRenderException):
    """Exception raised for errors in the render response data."""
    pass

