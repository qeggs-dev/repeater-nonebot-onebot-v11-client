from __future__ import annotations
import httpx
from nonebot.adapters.onebot.v11 import Message
import base64
import asyncio
from typing import AsyncGenerator, Generator, Any
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
    
    def get_images(self, skip_size: int = 10 * 1024 * 1024) -> Generator[str, None, None]:
        for segment in self._message:
            if segment.type == 'image':
                size = int(segment.data["file_size"])
                if size > skip_size:
                    continue
                yield str(segment.data["url"])

    async def download_image(self, skip_size: int = 10 * 1024 * 1024) -> AsyncGenerator[bytes | None, None]:
        """
        下载图片

        :param image_url: 图片链接
        :return Response[bytes | None]: 图片内容，如果图片大小超过skip_size，则返回None
        """

        for image in self.get_images(skip_size = skip_size):
            url = image
            response = await self._client.get(url)
            if response.status_code == 200:
                yield response.content
            else:
                yield None
    
    async def download_image_to_base64(self, skip_size: int = 1024 * 1024 * 10) -> AsyncGenerator[str | None, None]:
        """
        获取图片的base64编码

        :return: 图片的base64编码
        """
        async for image in self.download_image(skip_size):
            if image is not None:
                base64_result = (await asyncio.to_thread(base64.b64encode, image)).decode("utf-8")
                type_str = self.detect_image_type(image)
                output_buffer: list[str] = []
                output_buffer.append("data:")
                output_buffer.append(type_str)
                output_buffer.append(";base64,")
                output_buffer.append(base64_result)
                yield "".join(output_buffer),
            else:
                yield None
    
    async def close(self) -> None:
        await self._client.aclose()
    
    async def __aenter__(self) -> ImageDownloader:
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()