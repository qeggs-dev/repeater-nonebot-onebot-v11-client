from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message
from nonebot.params import CommandArg

comment = on_command("#", aliases={"anot", "annotation", "Annotation"}, rule=to_me(), block=True)

@comment.handle()
async def handle_annotation(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    return
