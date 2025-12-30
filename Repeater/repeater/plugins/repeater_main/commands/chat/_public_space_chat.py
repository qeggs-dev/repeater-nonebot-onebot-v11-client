from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment

from .._clients import ChatCore, ChatSendMsg
from ...assist import PersonaInfo
from ...logger import logger

public_space_chat = on_command("publicSpaceChat", aliases={"psc", "public_space_chat", "Public_Space_Chat", "PublicSpaceChat"}, rule=to_me(), block=True)

@public_space_chat.handle()
async def handle_public_space_chat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)

    logger.info(
        "Received a message {message} from {namespace}",
        message = persona_info.message_str,
        namespace = persona_info.namespace_str,
        module = "Chat.Public_Space_Chat"
    )

    message = persona_info.message

    chat_core = ChatCore(persona_info)
    
    images: list[str] = await persona_info.get_images_url()

    response = await chat_core.send_message(
        message.extract_plain_text().strip(),
        image_url = images
    )

    send_msg = ChatSendMsg(
        "Public_Space_Chat",
        persona_info,
        public_space_chat,
        response
    )
    await send_msg.send()