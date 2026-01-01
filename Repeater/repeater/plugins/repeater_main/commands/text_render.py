from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ..assist import PersonaInfo, SendMsg

text_render = on_command("textRender", aliases={"tr", "text_render", "Text_Render", "TextRender"}, rule=to_me(), block=True)

@text_render.handle()
async def handle_text_render(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)
    send_msg = SendMsg("Render.Markdown", text_render, persona_info)
    await send_msg.send_render(persona_info.message_str)