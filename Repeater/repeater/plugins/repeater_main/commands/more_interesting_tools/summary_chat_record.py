import asyncio
from ...assist import (
    PersonaInfo,
    SendMsg,
    MessageSource,
    Response
)
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from .._bases import BaseChat, SendMessage
from ...clients import ChatClient, ChatResponse


@CommandCaller.register
class SummaryChatRecord(BaseChat):
    cmd = "summaryChatRecord"
    aliases = {
        "scr",
        "SCR",
        "summary_chat_record",
        "Summary_Chat_Record",
        "SummaryChatRecord",
        "SUMMARY_CHAT_RECORD",
    }
    cmd_type = CmdTypes.OTHER
    acceptable_sources = {MessageSource.GROUP}

    
    async def parse_message(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
    ) -> SendMessage:
        group_id = persona_info.group_id

        try:
            n = int(persona_info.message_stripped_str)
        except (ValueError, TypeError):
            await send_msg.send_error("Please enter a valid number.")

        if n > 0:
            message_list = await persona_info.cached_api.get_group_msg_history(
                group_id=group_id,
                count=n
            )

            text = await asyncio.to_thread(
                persona_info.generates_text_from_messages_list,
                message_list["messages"]
            )

            if text:
                text = f"{text}\n\n---\n\nPlease summarize the above chat record."
            return SendMessage(
                text = text,
            )
        else:
            await send_msg.send_error("The input must be a positive integer!")
        
        send_msg.break_handler()