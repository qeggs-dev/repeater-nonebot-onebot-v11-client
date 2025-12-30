from nonebot import on_command
from nonebot.internal.matcher.matcher import Matcher
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from ...logger import logger

from .._clients import ChatCore, ChatSendMsg
from ...assist import PersonaInfo

chat: type[Matcher] = on_command("raw", aliases={"raw", "rawchat", "raw_chat", "Raw_Chat", "RawChat"}, rule=to_me(), block=True)

@chat.handle()
async def handle_raw_chat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)

    logger.info(
        "Received a message {message} from {namespace}",
        message = persona_info.message_str,
        namespace = persona_info.namespace_str,
        module = "Chat.Raw_Chat"
    )

    message = persona_info.message

    core = ChatCore(persona_info)

    images: list[str] = await persona_info.get_images_url()

    response = await core.send_message(
        message = message.extract_plain_text().strip(),
        add_metadata = False,
        image_url = images
    )

    send_msg = ChatSendMsg(
        "Chat.Chat",
        persona_info,
        chat,
        response
    )
    await send_msg.send()