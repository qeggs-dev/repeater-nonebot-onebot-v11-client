from __future__ import annotations
import httpx
from nonebot.adapters.onebot.v11 import Message
import base64
import asyncio
from typing import AsyncGenerator, Generator, Any
from ._response_body import Response
import imghdr

class ImageDownloader:
    def __init__(self, message: Message, timeout: float = 10.0) -> None:
        self._message = message
        self._client = httpx.AsyncClient(
            timeout = timeout,
        )
    
    @staticmethod
    def detect_image_type(content: bytes) -> str:
        """检测图片类型"""
        image_type = imghdr.what(None, content)
        type_map = {
            'jpeg': 'image/jpeg',
            'jpg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'bmp': 'image/bmp',
            'webp': 'image/webp'
        }
        return type_map.get(image_type, 'application/octet-stream')
    
    def get_images(self) -> Generator[dict[str, Any], None, None]:
        for segment in self._message:
            if segment.type == 'image':
                yield segment.data

    async def download_image(self, skip_size: int = 10 * 1024 * 1024) -> AsyncGenerator[Response[bytes | None], None]:
        """
        下载图片

        :param image_url: 图片链接
        :return Response[bytes | None]: 图片内容，如果图片大小超过skip_size，则返回None
        """

        for image in self.get_images():
            url = str(image["url"])
            size = int(image["file_size"])
            if size > skip_size:
                yield Response(
                    data = None,
                )
                continue
            response = await self._client.get(url)
            if response.status_code == 200:
                yield Response(
                    code = response.status_code,
                    text = response.text,
                    data = response.content
                )
            else:
                yield Response(
                    code = response.status_code,
                    text = response.text,
                    data = None,
                )
    
    async def download_image_to_base64(self, skip_size: int = 1024 * 1024 * 10) -> AsyncGenerator[Response[str | None], None]:
        """
        获取图片的base64编码

        :return: 图片的base64编码
        """
        async for image in self.download_image(skip_size):
            if image is not None:
                base64_result = (await asyncio.to_thread(base64.b64encode, image.data)).decode("utf-8")
                type_str = self.detect_image_type(image.data)
                output_buffer: list[str] = []
                output_buffer.append("data:")
                output_buffer.append(type_str)
                output_buffer.append(";base64,")
                output_buffer.append(base64_result)
                yield Response(
                    data = "".join(output_buffer),
                )
            else:
                yield Response(
                    data = None,
                )
    
    async def close(self) -> None:
        await self._client.aclose()
    
    async def __aenter__(self) -> ImageDownloader:
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()