from __future__ import annotations

import aiofiles

from nonebot import get_bots
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment, Message
from nonebot.internal.adapter.adapter import Adapter
from typing import AsyncGenerator, Container, Iterable

from nonebot.internal.adapter.bot import Bot
from ..assist_func import (
    at_with_name,
    image_to_text,
    get_images_url,
    get_reply_msgs,
    get_forward_msgs,
    get_message_event,
    generates_text_from_messages_list,
    get_reply_chain
)
from ..namespace import MessageSource, Namespace
from .enter_type import EnterType
from .file_info import FileInfo
from .cached_apis import CachedAPI
from ..user_config import UserConfigLoader, UserConfigs

class PersonaInfo:
    """
    Repeater 统一 Input 处理对象

    Usage:
    
        >>> from nonebot import on_command
        >>> from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
        >>> from nonebot.params import CommandArg
        >>> 
        >>> @on_command("my_command", aliases={"my_commmand_alias"}, priority=5)
        >>> async def my_command(
        ...     bot: Bot,
        ...     event: MessageEvent,
        ...     args: Message = CommandArg()
        ... ):
        ...     persona_info = PersonaInfo(bot, event, args)
        ...     if persona_info:
        ...         user_id = persona_info.user_id
        ...         group_id = persona_info.group_id
        ...         user_configs = await persona_info.get_user_configs()
        ...
        ...         async for ref in persona_info.from_reference_chain():
        ...             ref_user_id = ref.user_id
        ...             # do something
        ...             pass
        ...     else:
        ...         # empty message
        ...         pass
    """
    def __init__(
            self,
            bot: Bot,
            event: MessageEvent,
            args: str | Message | None = None
        ) -> None:
        """
        创建一个 PersonaInfo 对象
        
        :param bot: Bot 对象
        :param event: MessageEvent 对象
        :param args: Message 或 None，默认为 None
        """
        self._bot: Bot = bot
        self._cached_api: CachedAPI = CachedAPI(
            self._bot.adapter,
            self._bot.self_id
        )
        self._message_event: MessageEvent = event

        self._args: Message | None
        if isinstance(args, Message):
            self._args = args
        elif isinstance(args, str):
            self._args = Message(args)
        else:
            self._args = None
        
        self._group_id: str | None = None
        self._source: MessageSource = MessageSource.GROUP
        self._source = MessageSource(event.message_type.strip().lower())
        self._enter_type: EnterType = EnterType.Command
        self._raw_message_event: MessageEvent | None = None
        self._self_id: str = bot.self_id

        if self._source == MessageSource.GROUP:
            try:
                self._group_id = str(event.model_dump()["group_id"])
                if self._group_id is None:
                    raise ValueError("Is Group, But Group ID is None")
            except KeyError:
                raise ValueError("Is Group, But Group ID is Not Found")
        
        self._superusers: set[str] = set(user for user in self._bot.config.superusers)
        self._user_config_loader = UserConfigLoader(self.namespace)
    
    @classmethod
    def from_command(cls, bot: Bot, event: MessageEvent, args: Message | None = None) -> PersonaInfo:
        """
        从命令事件构建

        :param bot: Bot
        :param event: MessageEvent
        :param args: Message | None
        """
        persona_info = cls(
            bot = bot,
            event = event,
            args = args
        )
        persona_info._enter_type = EnterType.Command
        return persona_info
    
    @classmethod
    def from_message(cls, bot: Bot, event: MessageEvent) -> PersonaInfo:
        """
        从消息事件创建

        :param bot: 机器人实例
        :param event: 消息事件
        """
        persona_info = cls(
            bot = bot,
            event = event
        )
        persona_info._enter_type = EnterType.Message
        return persona_info
    
    @classmethod
    def from_horizontal(cls, persona_info: PersonaInfo) -> PersonaInfo:
        """
        从横向模式进入

        :param persona_info: 来自横向调用的 PersonaInfo
        """
        persona_info = cls(
            bot = persona_info.bot,
            event = persona_info.event,
            args = persona_info.args
        )
        persona_info._enter_type = EnterType.Horizontal
        return persona_info
    
    def copy(self) -> PersonaInfo:
        """
        复制一份
        """
        return self.__class__(
            bot = self.bot,
            event = self.event,
            args = self.args
        )
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, PersonaInfo):
            return (
                self._bot == other._bot and
                self._message_event == other._message_event and
                self._args == other._args
            )
        return False
    
    def copy_with_args(self, args: Message | str | None = None) -> PersonaInfo:
        """
        复制一份，并自定义 args
        """
        return self.__class__(
            bot = self.bot,
            event = self.event,
            args = args if args is not None else self.args
        )
    
    async def from_message_event(self, event: MessageEvent | None) -> PersonaInfo:
        """
        从 MessageEvent 构建 PersonaInfo
        """
        if event is None:
            event = await self.get_message_event()
        cls = type(self)
        instance = cls(
            bot = self.bot,
            event = event,
            args = self.args,
        )
        instance._enter_type = self._enter_type
        return instance

    async def from_reference_reversed_chain(self) -> list[PersonaInfo]:
        """
        从引用链构建 PersonaInfo 实例，且反向

        注：解析时，它会默认消息段中只有一个 reply 消息段，
        如果有存在多个，则使用第一个
        """
        reference_chain: list[PersonaInfo] = []
        async for persona_info in self.from_reference_chain():
            reference_chain.append(persona_info)
        return reference_chain[::-1]
    
    async def from_reference_chain(self) -> AsyncGenerator[PersonaInfo, None]:
        """
        从引用链构建 PersonaInfo 实例

        注：解析时，它会默认消息段中只有一个 reply 消息段，
        如果有存在多个，则使用第一个
        """
        cls = type(self)
        async for event in self.get_reply_chain():
            persona_info = cls(
                bot = self.bot,
                event = event
            )
            yield persona_info
    
    async def from_reference(self) -> PersonaInfo | None:
        """
        从回复引用构建 PersonaInfo 实例

        注：解析时，它会默认消息段中只有一个 reply 消息段，
        如果有存在多个，则使用第一个
        """
        event = await self.get_message_event()
        reply_id: str | None = None
        for message in event.message:
            if message.type == "reply":
                reply_id = message.data["id"]
                break
        if reply_id is None:
            return None
        reply_event = await self.get_message_event(message_id = int(reply_id))
        persona_info = self.__class__(
            bot = self.bot,
            event = reply_event
        )
        return persona_info
    
    def namespace_from_this_group(self, user_id: str) -> Namespace:
        """
        基于当前群组信息，构建指定 user_id 的 Namespace 实例
        """
        if self._source == MessageSource.GROUP:
            return Namespace(
                mode = MessageSource.GROUP,
                group_id = self._group_id,
                user_id = user_id
            )
        else:
            return Namespace(
                mode = MessageSource.PRIVATE,
                user_id = user_id
            )
    
    @property
    def enter_type(self) -> EnterType:
        """
        获取进入模式
        """
        return self._enter_type
    
    def __bool__(self) -> bool:
        """
        判断消息是否为空
        """
        for message in self.message:
            if message.type == "text":
                if message.data["text"]:
                    return True
            elif message.type not in ["at", "reply"]:
                return True
        return False
    
    @property
    def adapter(self) -> Adapter:
        """
        获取 Bot 的 Adapter 实例
        """
        return self._bot.adapter
    
    @property
    def is_superuser(self) -> bool:
        """
        当前发起请求的用户是否为超级用户
        """
        if self._bot.config.superusers is None:
            return False
        return self.user_id in self.superusers
    
    @property
    def is_self(self) -> bool:
        """
        当前发起请求的用户是否为自身
        """
        return self.user_id == self.self_id
    
    @property
    def self_id(self) -> str:
        """
        机器人自身 ID
        """
        return self._self_id
    
    @property
    def superusers(self) -> set[str]:
        """
        超级用户集合
        """
        return self._superusers.copy()
    
    @property
    def message_id(self) -> int:
        """
        当前消息 ID
        """
        return self._message_event.message_id

    @property
    def group_id(self) -> str | None:
        """
        当前群号
        """
        if self._group_id is None:
            return None
        return self._group_id
    
    @property
    def user_id(self) -> str:
        """
        当前用户 ID
        """
        return str(self._message_event.user_id)
    
    @property
    def nickname(self) -> str | None:
        """
        当前用户昵称
        """
        return self._message_event.sender.nickname
    
    @property
    def card(self) -> str | None:
        """
        当前用户名片

        通常情况下，群名片会覆盖昵称
        """
        return self._message_event.sender.card
    
    @property
    def display_name(self) -> str:
        """
        当前用户显示名称

        自动处理用户昵称、群名片
        """
        if self.card:
            return self.card
        else:
            if self.nickname is not None:
                return self.nickname
            return ""
    
    @property
    def age(self) -> int | None:
        """
        当前用户年龄
        """
        return self._message_event.sender.age
    
    @property
    def gender(self) -> str | None:
        """
        当前用户性别
        """
        return self._message_event.sender.sex
    
    @property
    def bot(self) -> Bot | Bot:
        """
        Bot 实例
        """
        return self._bot
    
    @property
    def cached_api(self) -> CachedAPI:
        """
        Bot 实例（带 API 请求缓存）
        """
        return self._cached_api
    
    @property
    def bots(self) -> dict[str, Bot]:
        """
        所有 Bot 实例
        """
        return get_bots()
    
    @property
    def event(self) -> MessageEvent:
        """
        消息事件对象
        """
        return self._message_event

    @property
    def namespace(self) -> Namespace:
        """
        当前用户所在命名空间
        """
        if self._source == MessageSource.GROUP:
            return Namespace(
                mode = MessageSource.GROUP,
                group_id = self._group_id,
                user_id = self.user_id
            )
        else:
            return Namespace(
                mode = MessageSource.PRIVATE,
                user_id = self.user_id
            )
    
    @property
    def namespace_str(self) -> str:
        """
        当前用户所在命名空间字符串
        """
        return self.namespace.namespace_str
    
    @property
    def private_namespace(self) -> Namespace:
        """
        当前用户所在命名空间（私聊）
        """
        return Namespace(
            mode = MessageSource.PRIVATE,
            user_id = self.user_id
        )
    
    @property
    def private_namespace_str(self) -> str:
        """
        当前用户所在命名空间字符串（私聊）
        """
        return self.private_namespace.namespace_str

    def group_namespace(self, group_id: str | None = None) -> Namespace:
        """
        当前用户所在命名空间（群聊）
        """
        if group_id is None and self._group_id is None:
            raise RuntimeError("Not found group_id")
        return Namespace(
            mode = MessageSource.GROUP,
            group_id = group_id or self._group_id,
            user_id = self.user_id
        )
    
    def group_namespace_str(self, group_id: str | None = None) -> str:
        """
        当前用户所在命名空间字符串（群聊）
        """
        return self.group_namespace(group_id).namespace_str
    
    @property
    def public_namespace_str(self) -> str:
        """
        当前用户所在命名空间字符串（公共空间）
        """
        return self.namespace.public_space_id
    
    async def get_user_configs(self) -> UserConfigs:
        """
        获取用户配置
        """
        return await self._user_config_loader.load()
    
    async def set_user_configs(self, configs: UserConfigs):
        """
        设置用户配置
        """
        await self._user_config_loader.save(configs)
    
    @property
    def event_message(self) -> Message:
        """
        来自事件的消息
        """
        return self._message_event.message
    
    @property
    def message(self) -> Message:
        """
        消息内容

        如果存在 args 就使用 args，否则使用 event_message
        """
        if self._args is not None:
            return self._args.copy()
        else:
            return self._message_event.message.copy()
    
    @property
    def args(self) -> Message:
        """
        命令参数
        """
        if self._args is not None:
            return self._args.copy()
        else:
            return Message()
    
    @property
    def event_message_str(self) -> str:
        """
        消息事件字符串
        """
        return self.event_message.extract_plain_text()
    
    @property
    def message_str(self) -> str:
        """
        消息字符串
        """
        return self.message.extract_plain_text()
    
    @property
    def message_striped_str(self) -> str:
        """
        消息字符串（去除首尾空格）
        """
        return self.message_str.strip()
    
    @property
    def event_message_striped_str(self) -> str:
        """
        消息事件字符串（去除首尾空格）
        """
        return self.event_message_str.strip()
    
    @property
    def args_str(self) -> str:
        """
        命令参数字符串
        """
        return self.args.extract_plain_text()
    
    @property
    def reply(self) -> MessageSegment:
        """
        引用当前消息的消息段
        """
        return MessageSegment.reply(self.message_id)
    
    @property
    def source(self) -> MessageSource:
        """
        消息来源
        """
        return self._source
    
    @property
    def noself_at_list(self) -> list[str]:
        """
        消息中提及的 QQ 号列表（不包括自己）
        """
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
    def at_list(self) -> list[str]:
        """
        消息中提及的 QQ 号列表
        """
        at_list: list[str] = []
        if self._message_event is None:
            return at_list
        for segment in self._message_event.message:
            if segment.type == "at":
                at_list.append(segment.data["qq"])
        return at_list
    
    async def handle_at_with_name(self) -> Message:
        """
        处理@消息，将@的QQ号替换为昵称
        """
        return await at_with_name(self._cached_api, self._message_event)
    
    async def image_to_text(self, format: str = "{text}", cite: bool = True, excluded_tags:Container[str] = {}) -> Message:
        """
        将消息内的图片消息段通过 OCR 转换为文字
        """
        return await image_to_text(
            self._cached_api,
            self.message,
            format = format,
            cite = cite,
            excluded_tags = excluded_tags
        )
    
    @property
    def plaintext_message(self) -> str:
        """
        消息的纯文本内容
        """
        return self.message.extract_plain_text()
    
    async def get_images_url(self, base64: bool | None = None) -> list[str]:
        """
        获取消息内的图片消息段

        :param base64: 是否返回 base64 编码的图片
        :return: 图片的 URL 列表
        """
        return await get_images_url(
            self.message,
            base64 = base64
        )
    
    def get_video_url(self) -> list[str]:
        """
        获取消息内的视频消息段

        :return: 视频的 URL 列表
        """
        urls: list[str] = []
        for msg in self.message:
            if msg.type == "video":
                urls.append(msg.data["url"])
        return urls
    
    def get_audio_url(self) -> list[str]:
        """
        获取消息内的音频消息段

        :return: 音频的 URL 列表
        """
        urls: list[str] = []
        for msg in self.message:
            if msg.type == "record":
                urls.append(msg.data["url"])
        return urls
    
    def get_file_ids(self) -> list[str]:
        """
        获取消息内的文件消息段

        :return: 文件的 URL 列表
        """
        ids: list[str] = []
        for msg in self.message:
            if msg.type == "file":
                ids.append(msg.data["file_id"])
        return ids
    
    def get_file_urls(self) -> list[str]:
        """
        获取消息内的文件消息段

        :return: 文件的 URL 列表
        """
        urls: list[str] = []
        for msg in self.message:
            if msg.type == "file":
                urls.append(msg.data["url"])
        return urls
    
    async def get_file_info(self, file_id: str) -> FileInfo:
        """
        根据文件 ID

        :param file_id: 文件 ID
        """
        response = await self._cached_api.get_file(file = file_id)
        return FileInfo(**response)
    
    async def get_file_name(self, file_id: str) -> str:
        """
        获取文件名

        :param file_id: 文件 ID
        :return: 文件名
        """
        file_info = await self.get_file_info(file_id)
        return file_info.file_name
    
    async def get_file_size(self, file_id: str) -> int:
        """
        获取文件大小

        :param file_id: 文件 ID
        :return: 文件大小
        """
        file_info = await self.get_file_info(file_id)
        return int(file_info.file_size)
    
    async def open_file(self, file_info: FileInfo) -> bytes:
        """
        打开文件

        :param file_info: 文件信息
        :return: 文件内容
        """
        async with aiofiles.open(file_info.file, "rb") as f:
            return await f.read()
    
    async def open_text_file(self, file_info: FileInfo, encoding: str = "utf-8") -> str:
        """
        打开文本文件

        :param file_info: 文件信息
        :param encoding: 编码
        :return: 文件内容
        """
        async with aiofiles.open(file_info.file, "r", encoding = encoding) as f:
            return await f.read()
    
    async def get_reply_chain(self) -> AsyncGenerator[MessageEvent, None]:
        """
        获取回复链

        注：解析时，它会默认消息段中只有一个 reply 消息段，
        如果有存在多个，则使用第一个
        """

        # 经过框架处理的 Event 中可能并未包含 reply 消息段
        # 需要重新获取原始 Event
        event = await self.get_message_event()
        message: Message = event.message

        chain = get_reply_chain(
            self._cached_api,
            message
        )
        async for msg in chain:
            yield msg
    
    async def get_reply_msgs(self, message: Message | None = None) -> list[MessageEvent]:
        """
        获取回复消息

        :param message: 消息
        :return: 回复消息
        """
        return await get_reply_msgs(
            self._cached_api,
            message if message is not None else self.message
        )
    
    async def get_forward_msgs(self) -> list[MessageEvent]:
        """
        获取转发消息

        :return: 转发消息
        """
        return await get_forward_msgs(
            self._cached_api,
            self.message
        )
    
    @staticmethod
    def generates_text_from_messages_list(messages: Iterable[dict | MessageEvent]) -> str:
        """
        从消息列表生成文本

        :param messages: 消息列表
        :return: 文本
        """
        return generates_text_from_messages_list(messages)
    
    async def get_message_event(self, message_id: int | None = None) -> MessageEvent:
        """
        获取消息事件 (并非框架报告给 Repeater 的消息事件)

        :param message_id: 消息id
        :return: 消息事件
        """
        return await get_message_event(
            bot = self._cached_api,
            message_id = message_id if message_id is not None else self.message_id
        )