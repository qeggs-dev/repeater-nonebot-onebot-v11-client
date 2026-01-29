from nonebot.adapters.onebot.v11 import MessageSegment, Message
from nonebot.internal.matcher.matcher import Matcher
from ....assist import PersonaInfo, MessageSource, Response, SendMsg
from ._response_body import ChatResponse
from ....chattts import ChatTTSAPI
from typing import NoReturn, Type
from ....logger import logger as base_logger
import numpy as np

logger = base_logger.bind(module = "Chat.SendMsg")

class ChatSendMsg(SendMsg):
    def __init__(
            self,
            component: str,
            persona_info: PersonaInfo,
            matcher: Type[Matcher],
            response: Response[ChatResponse],
        ):
        super().__init__(component, matcher, persona_info)
        self._response: Response[ChatResponse] = response
        self._chat_tts_api = ChatTTSAPI()
    
    async def _send_error_message(self) -> NoReturn:
        if self._response.get_data() is None:
            await self.send_response(
                self._response
            )
        else:
            await self.send_response(
                self._response,
                message = self._response.get_data().content
            )


    async def send(self):
        if self._response.code == 200 and self._response.get_data() is not None:
            score = self.text_length_score(self._response.get_data().content)
            threshold = self.text_length_score_threshold
            logger.info(f"Response content socre: {score}")
            if score >= threshold:
                logger.warning(f"Response content socre to high: {score}, Expected to be below {threshold} ")
                logger.warning("The text will be rendered as an image output.")
                await self.send_image_mode()
            else:
                await self.send_text_mode()
        else:
            await self.send_error_response(self._response)
    
    async def send_tts_mode(self, text: str | None = None) -> NoReturn:
        if self.is_debug_mode:
            await self.send_debug_mode()
        else:
            if self._response.code == 200 and self._response.get_data() is not None:
                if self._response.get_data().reasoning_content:
                    await self.send_render(
                        self._response.get_data().reasoning_content,
                        reply = True,
                        continue_handler = True
                    )
                if self._response.get_data().content:
                    await self.send_tts(
                        text or self._response.get_data().content,
                        reply = False,
                        continue_handler = False
                    )
            else:
                await self.send_error_response(self._response)
            
    
    async def send_text_mode(self, text: str | None = None) -> NoReturn:
        if self.is_debug_mode:
            await self.send_debug_mode()
        else:
            if self._response.code == 200 and self._response.get_data() is not None:
                message = Message()
                message.append(self._persona_info.reply)
                # 推理内容必须渲染为图片
                if self._response.get_data().reasoning_content:
                    message.append(
                        await self.text_render(self._response.get_data().reasoning_content)
                    )
                if self._response.get_data().content:
                    message.append(text or self._response.get_data().content)
                else:
                    message.append("Message is empty.")
                await self._matcher.finish(message)
            else:
                await self.send_error_response(self._response)
    
    async def send_image_mode(self, text: str | None = None) -> NoReturn:
        if self.is_debug_mode:
            await self.send_debug_mode()
        else:
            if self._response.code == 200 and self._response.get_data() is not None:
                message = Message()
                message.append(self._persona_info.reply)
                if self._response.get_data().reasoning_content:
                    message.append(
                        await self.text_render(self._response.get_data().reasoning_content)
                    )
                if self._response.get_data().content:
                    message.append(
                        await self.text_render(self._response.get_data().content)
                    )
                else:
                    message.append("[Message is empty.]")
                await self._matcher.finish(message)
            else:
                await self.send_error_response(self._response)