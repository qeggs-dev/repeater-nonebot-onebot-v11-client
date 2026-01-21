import asyncio
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent
from nonebot.params import CommandArg
from pydantic import ValidationError

from ...assist import PersonaInfo, SendMsg, MessageSource
from .._clients import ChatCore, ChatSendMsg

summary_chat_record = on_command("summaryChatRecord", aliases={"scr", "summary_chat_record", "Summary_Chat_Record", "SummaryChatRecord"}, rule=to_me(), block=True)

def generate_text(messages: list[dict]):
    text_buffer: list[str] = []
    validation_failure_counter: int = 0
    for message in messages["messages"]:
        try:
            event = MessageEvent(**message)
            nick_name = event.sender.card or event.sender.nickname
            text = f"{nick_name}: {event.message}\n"
        except ValidationError:
            try:
                nick_name = message["sender"]["card"] or message["sender"]["nickname"]
                text = f"{nick_name}: {message['message']}\n"
            except KeyError:
                validation_failure_counter += 1
                continue
        
        text_buffer.append(
            f"{nick_name}: {text}"
        )

    if validation_failure_counter > 0:
        text_buffer.append(f"Validation Failure: {validation_failure_counter}")
    text_buffer.append("---")
    text_buffer.append("Please summarize the above chat record.")
    return "\n".join(text_buffer)


@summary_chat_record.handle()
async def handle_summary_chat_record(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)
    send_msg = SendMsg("More.Summary_Chat_Record", summary_chat_record, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    
    if persona_info.source == MessageSource.PRIVATE:
        await send_msg.send_error("The current feature cannot be used in private chat.")
    
    group_id = persona_info.group_id
    
    try:
        n = int(args.extract_plain_text())
    except (ValueError, TypeError):
        await send_msg.send_error("Please enter a valid number.")
    if n > 0:
        message_list = await bot.get_group_msg_history(
            group_id = group_id,
            count = n
        )

        text = await asyncio.to_thread(generate_text, message_list)

        chat_core = ChatCore(persona_info, namespace = "Summary_Chat_Record")
        response = await chat_core.send_message(
            add_metadata = False,
            message = text,
            save_context = False
        )
        chat_sendmsg = ChatSendMsg(
            send_msg.component,
            persona_info,
            summary_chat_record,
            response
        )
        await chat_sendmsg.send()
        
    else:
        await send_msg.send_error("The input must be a positive integer!")