from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment, Message
from typing import Literal, Container
from ._assist_func import (
    handle_at_with_name,
    image_to_text
)
from ..core_net_configs import storage_configs
from ._namespace import MessageSource, Namespace
from ._image_downloader import ImageDownloader

class PersonaInfo:
    def __init__(self, bot: Bot, event: MessageEvent, args: Message | None = None):
        self._bot: Bot = bot
        self._message_event: MessageEvent = event
        self._args: Message | None = args
        self._group_id: int | None = None
        self._source: MessageSource = MessageSource.GROUP
        
        self._source = MessageSource(event.message_type.strip().lower())

        if self._source == MessageSource.GROUP:
            try:
                self._group_id = int(event.model_dump()["group_id"])
                if self._group_id is None:
                    raise ValueError("Is Group, But Group ID is None")
            except KeyError:
                raise ValueError("Is Group, But Group ID is Not Found")
        
        self._superusers: set[int] = set(int(user) for user in self._bot.config.superusers)
    
    def __bool__(self) -> bool:
        for message in self.message:
            if message.type not in  ["at", "text", "reply"]:
                return True
            if message.type == "text":
                if message.data["text"]:
                    return True
        return False
    
    @property
    def is_superuser(self) -> bool:
        if self._bot.config.superusers is None:
            return False
        return self.user_id in self.superusers
    
    @property
    def superusers(self) -> set[int]:
        return self._superusers.copy()
    
    @property
    def message_id(self) -> int:
        return self._message_event.message_id

    @property
    def group_id(self) -> int | None:
        if self._group_id is None:
            return None
        return self._group_id
    
    @property
    def user_id (self) -> int:
        return self._message_event.user_id
    @property
    def nickname(self) -> str | None:
        return self._message_event.sender.nickname
    
    @property
    def card(self) -> str | None:
        return self._message_event.sender.card
    
    @property
    def display_name(self) -> str:
        if self.card:
            return self.card
        else:
            if self.nickname is not None:
                return self.nickname
            return ""
    
    @property
    def age(self) -> int | None:
        return self._message_event.sender.age
    
    @property
    def gender(self) -> str | None:
        return self._message_event.sender.sex
    
    @property
    def bot(self):
        return self._bot

    @property
    def namespace(self):
        if self._source == MessageSource.GROUP:
            return Namespace(
                mode=MessageSource.GROUP,
                group_id=self._group_id,
                user_id=self.user_id
            )
        else:
            return Namespace(
                mode=MessageSource.PRIVATE,
                user_id=self.user_id
            )
    
    @property
    def namespace_str(self):
        return self.namespace.namespace
    
    @property
    def public_namespace_str(self) -> str:
        return self.namespace.public_space_id
    
    @property
    def event_message(self) -> Message:
        return self._message_event.message
    
    @property
    def message(self) -> Message:
        if self._args is not None:
            return self._args.copy()
        else:
            return self._message_event.message.copy()
    
    @property
    def args(self) -> Message:
        if self._args is not None:
            return self._args.copy()
        else:
            return Message()
    
    @property
    def message_str(self) -> str:
        return self.message.extract_plain_text()
    
    @property
    def args_str(self) -> str:
        return self.args.extract_plain_text()
    
    @property
    def reply(self):
        return MessageSegment.reply(self.message_id)
    
    @property
    def source(self) -> MessageSource:
        return self._source
    
    @property
    def noself_at_list(self):
        at_list: list[str] = []
        if self._message_event is None:
            return at_list
        for segment in self._message_event.message:
            if segment.type == "at":
                mentioned_id = segment.data["qq"]
                # 检查是否@的是非机器人用户
                if mentioned_id != self._bot.self_id:
                    at_list.append(mentioned_id)
        return at_list
    
    @property
    def at_list(self):
        at_list: list[str] = []
        if self._message_event is None:
            return at_list
        for segment in self._message_event.message:
            if segment.type == "at":
                at_list.append(segment.data["qq"])
        return at_list
    
    async def handle_at_with_name(self):
        return await handle_at_with_name(self._bot, self._message_event)
    
    async def image_to_text(self, format: str = "{text}", cite: bool = True, excluded_tags:Container[str] = {}) -> Message:
        """将图片转换为文字"""
        if "image" not in self.message:
            return self.message
        outmsg = Message()
        for segment in self.message:
            if segment.type == "image":
                ocrout = await self._bot.ocr_image(image = segment.data["url"])
                text = ""
                tag = segment.data.get("summary", "")
                for item in ocrout:
                    text += item["text"] + "\n"
                if text.endswith("\n"):
                    text = text[:-1]
                if tag not in excluded_tags:
                    text = f"[Image tag:{tag}]\n{text}"
                if text.strip():
                    text = format.format(text = text)
                    if cite:
                        text = text.replace("\n", "\n> ")
                    outmsg.append(MessageSegment(type = "text", data = {"text": text}))
                else:
                    outmsg.append(segment)
            else:
                outmsg.append(segment)
        return outmsg
    
    @property
    def plaintext_message(self) -> str:
        return self.message.extract_plain_text()
    
    async def get_images_url(self, base64: bool | None = None) -> list[str]:
        if base64 is None:
            base64 = storage_configs.use_base64_visual_input
        images: list[str] = []
        if "image" in self.message:
            async with ImageDownloader(
                self.message,
                timeout=storage_configs.download_visual_input_timeout
            ) as downloader:
                if base64:
                    get_image_url = downloader.download_image_to_base64()
                    async for image_url in get_image_url:
                        if image_url is not None:
                            images.append(
                                image_url
                            )
                else:
                    for image_url in downloader.get_images():
                        images.append(image_url)
        return images