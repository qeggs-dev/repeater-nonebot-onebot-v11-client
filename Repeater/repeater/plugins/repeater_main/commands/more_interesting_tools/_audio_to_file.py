from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
from nonebot.params import (
    CommandArg,
    Arg
)
from ...assist import PersonaInfo, FileSender, FileUrl
import time

audio_to_file = on_command("audioToFile", aliases={"a2f", "audio_to_file", "Audio_To_File", "AudioToFile"}, rule=to_me(), block=True)

@audio_to_file.handle()
async def audio_to_file_handle(matcher: Matcher, args: Message = CommandArg()):
    if "record" in args:
        matcher.set_arg("echo_text", args)

@audio_to_file.got("record", prompt="Please send an audio message...")
async def audio_to_file_got(bot: Bot, event: MessageEvent, message: Message = Arg("record")):
    persona_info = PersonaInfo(bot = bot, event = event, args = message)
    for message_segment in persona_info.message:
        if message_segment.type == "record":
            file_sender = FileSender(persona_info=persona_info)
            fileurl = FileUrl(message_segment.data["url"])
            await file_sender.send_file(
                url = str(fileurl),
                file_name = f"{persona_info.nickname}_{time.strftime('%Y%m%d_%H%M%S', time.localtime())}{fileurl.path.suffix}"
            )