from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment

from .._clients import ChatCore, ChatSendMsg
from ...assist import PersonaInfo, SendMsg
from ...logger import logger

public_space_chat = on_command("publicSpaceChat", aliases={"psc", "public_space_chat", "Public_Space_Chat", "PublicSpaceChat"}, rule=to_me(), block=True)

@public_space_chat.handle()
async def handle_public_space_chat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)
    send_msg = SendMsg(
        "Chat.Public_Space_Chat",
        public_space_chat,
        persona_info
    )

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    logger.info(
        "Received a message {message} from {namespace}",
        message = persona_info.message_str,
        namespace = persona_info.namespace_str,
        module = send_msg.component_name
    )

    message = persona_info.message

    chat_core = ChatCore(persona_info)
    
    images: list[str] = await persona_info.get_images_url()

    response = await chat_core.send_message(
        message.extract_plain_text().strip(),
        image_url = images
    )

    send_msg = ChatSendMsg(
        send_msg.persona_info,
        persona_info,
        public_space_chat,
        response
    )
    await send_msg.send()