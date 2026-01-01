from nonebot import on_command
from nonebot.internal.matcher.matcher import Matcher
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from ...logger import logger

from .._clients import ChatCore, ChatSendMsg
from ...assist import PersonaInfo, SendMsg

chat: type[Matcher] = on_command("chat", aliases={"c", "Chat"}, rule=to_me(), block=True)

@chat.handle()
async def handle_chat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)
    send_msg = SendMsg(
        "Chat.Chat",
        chat,
        persona_info
    )

    if send_msg.is_debug_mode:
        send_msg.send_debug_mode()

    logger.info(
        "Received a message {message} from {namespace}",
        message = persona_info.message_str,
        namespace = persona_info.namespace_str,
        module = send_msg.component
    )

    message = persona_info.message

    core = ChatCore(persona_info)

    images: list[str] = await persona_info.get_images_url()

    response = await core.send_message(
        message = message.extract_plain_text().strip(),
        image_url = images
    )

    send_msg = ChatSendMsg(
        send_msg.component,
        persona_info,
        chat,
        response
    )
    await send_msg.send_text_mode()