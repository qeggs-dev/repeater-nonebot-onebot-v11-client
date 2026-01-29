from ._config import tts_config
from ..assist import Response
from ._tts_response import TTSResponse
import httpx

class ChatTTSAPI:
    def __init__(self):
        url = tts_config.base_url.rstrip("/")
        self.client = httpx.AsyncClient(base_url = url, timeout = tts_config.timeout)
    
    async def text_to_speech(self, text: str) -> Response[TTSResponse]:
        api_args = tts_config.api_args.model_dump()
        response = await self.client.post(
            "/tts",
            data={
                **api_args,
                "text": text,
                "skip_refine": 1 if tts_config.api_args.skip_refine else 0,
                "is_stream": 1 if tts_config.api_args.is_stream else 0,
            },
        )

        return Response(
            response,
            model = TTSResponse
        )
        