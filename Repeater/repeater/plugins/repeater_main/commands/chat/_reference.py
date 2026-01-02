from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment

from .._clients import ChatCore, ChatSendMsg
from ...assist import PersonaInfo, SendMsg
from ...logger import logger

reference = on_command("Reference", aliases={"ref", "Reference"}, rule=to_me(), block=True)

@reference.handle()
async def handle_reference(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)
    send_msg = SendMsg(
        "Chat.Reference",
        reference,
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

    message = persona_info.message

    chat_core = ChatCore(persona_info)

    images: list[str] = await persona_info.get_images_url()

    if not persona_info.noself_at_list:
        await send_msg.send_error("Please at a member to get reference.")
        
    response = await chat_core.send_message(
        message = message.extract_plain_text().strip(),
        reference_context_id=persona_info.noself_at_list[0],
        image_url = images
    )

    send_msg = ChatSendMsg(
        send_msg.component,
        persona_info,
        reference,
        response
    )
    await send_msg.send()
