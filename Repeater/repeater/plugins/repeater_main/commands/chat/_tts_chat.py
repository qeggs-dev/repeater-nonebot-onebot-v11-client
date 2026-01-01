from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message
from nonebot.params import CommandArg

from ...assist import PersonaInfo, SendMsg
from ...chattts import ChatTTSAPI
from .._clients import ChatCore, ChatSendMsg
from ...logger import logger

api = ChatTTSAPI()

tts_chat = on_command("tts_chat", aliases={"ttsc", "tts_Chat", "TTS_Chat"}, rule=to_me(), block=True)

@tts_chat.handle()
async def handle_tts_chat(bot: Bot, event: MessageEvent, args: Message = CommandArg()) -> None:
    persona_info = PersonaInfo(bot, event, args)
    send_msg = SendMsg(
        "Chat.TTS_Chat",
        tts_chat,
        persona_info
    )

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    logger.info(
        "Received a message {message} from {namespace}",
        message = persona_info.message_str,
        namespace = persona_info.namespace_str,
        module = send_msg.component
    )

    core = ChatCore(persona_info)

    images: list[str] = await persona_info.get_images_url()

    response = await core.send_message(
        message = persona_info.message_str,
        image_url = images
    )

    send_msg = ChatSendMsg(
        send_msg.component,
        persona_info = persona_info,
        matcher = tts_chat,
        response = response
    )
    await send_msg.send_tts_mode()