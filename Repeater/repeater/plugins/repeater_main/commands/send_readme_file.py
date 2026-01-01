from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ..core_net_configs import *
from ..assist import PersonaInfo, FileSender

seed_readme_file = on_command("sendReadmeFile", aliases={"srf", "send_readme_file", "Send_Readme_File", "SendReadmeFile"}, rule=to_me(), block=True)

@seed_readme_file.handle()
async def handle_send_readme_file(bot: Bot, event: MessageEvent):
    persona_info = PersonaInfo(bot=bot, event=event)

    sfurl = f"{HTML_README_FILE_ROUTE}"
    if RepeaterDebugMode:
        await seed_readme_file.finish(persona_info.reply + f"[Chat.Send_Readme_File|{persona_info.name_space.namespace}:{sfurl}]")
    else:
        file_sender = FileSender(sfurl)

        await file_sender.send_file(
            sfurl,
            "README.html"
        )