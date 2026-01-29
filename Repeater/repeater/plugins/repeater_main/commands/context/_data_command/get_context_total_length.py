from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ..._clients import ContextCore
from ....assist import PersonaInfo, SendMsg

get_context_total_length = on_command("getContextTotalLength", aliases={"gctl", "get_context_total_length", "Get_Context_Total_Length", "GetContextTotalLength"}, rule=to_me(), block=True)

@get_context_total_length.handle()
async def handle_total_context_length(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Context.Get_Context_Total_Length", get_context_total_length, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    
    context_core = ContextCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await context_core.get_context_total_length()

        if response.code == 200:
            data = response.get_data()
            if data is None:
                await send_msg.send_error("Unable to process data.")
            await send_msg.send_prompt(
                f"length: {data.context_length}\n"
                f"total_text_length: {data.total_context_length}\n"
                f"average_content_length: {data.average_content_length}\n"
            )
        else:
            await send_msg.send_response_check_code(response, "Get Context Total Length Failed")