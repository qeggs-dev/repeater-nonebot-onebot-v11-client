from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .._clients import UserFileCore
from ...assist import PersonaInfo, FileSender, SendMsg

send_user_data_file = on_command("sendUserDataFile", aliases={"sudf", "send_user_data_file", "Send_User_Data_File", "SendUserDataFile"}, rule=to_me(), block=True)

@send_user_data_file.handle()
async def handle_send_user_data_file(bot: Bot, event: MessageEvent):
    persona_info = PersonaInfo(bot=bot, event=event)
    send_msg = SendMsg("UserFile.Send_User_Data_File", send_user_data_file, persona_info)

    user_file_core = UserFileCore(persona_info)
    sfurl = await user_file_core.get_user_data_file_url()
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        file_sender = FileSender(persona_info)

        await file_sender.send_file(sfurl, f"{persona_info.namespace_str}_UserDataFile.zip")
