from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment

from .._clients import ChatCore, ChatSendMsg
from ...assist import PersonaInfo, SendMsg
from ...logger import logger
from ...core_net_configs import storage_configs

keep_reasoning = on_command("keepReasoning", aliases={"kr", "keep_reasoning", "Keep_Reasoning", "KeepReasoning"}, rule=to_me(), block=True)

@keep_reasoning.handle()
async def handle_keep_reasoning(bot: Bot, event: MessageEvent):
    persona_info = PersonaInfo(bot, event)
    send_msg = SendMsg(
        "Chat.Keep_Reasoning",
        keep_reasoning,
        persona_info
    )

    if send_msg.is_debug_mode:
        send_msg.send_debug_mode()

    logger.info(
        "Received a message from {namespace}",
        namespace = persona_info.namespace_str,
        module = send_msg.component
    )

    chat_core = ChatCore(persona_info)

    response = await chat_core.send_message(
        model_uid = storage_configs.reason_model_uid
    )
    
    send_msg = ChatSendMsg(
        send_msg.component,
        persona_info,
        keep_reasoning,
        response
    )
    await send_msg.send()
