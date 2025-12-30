from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment

from .._clients import ChatCore, ChatSendMsg
from ...assist import PersonaInfo
from ...logger import logger
from ...core_net_configs import storage_configs

reason = on_command("reason", aliases={"r", "Reason"}, rule=to_me(), block=True)

@reason.handle()
async def reason_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)

    logger.info(
        "Received a message {message} from {namespace}",
        message = persona_info.message_str,
        namespace = persona_info.namespace_str,
        module = "Chat.Reason"
    )

    message = persona_info.message

    chat_core = ChatCore(persona_info)

    images: list[str] = await persona_info.get_images_url()
    
    response = await chat_core.send_message(
        message = message.extract_plain_text().strip(),
        model_uid=storage_configs.reason_model_uid,
        image_url = images
    )
    
    send_msg = ChatSendMsg(
        "Reason",
        persona_info,
        reason,
        response
    )
    await send_msg.send()