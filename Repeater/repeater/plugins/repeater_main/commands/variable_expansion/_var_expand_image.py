from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .._clients import VariableExpansionCore
from ...assist import PersonaInfo, SendMsg

var_expand_image = on_command("varExpandImage", aliases={"vei", "var_expand_image", "Var_Expand_Image", "VarExpandImage"}, rule=to_me(), block=True)

@var_expand_image.handle()
async def handle_var_expand_image(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("VarExpandImage", var_expand_image, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    msg = args.extract_plain_text().strip()

    variable_expansion_core = VariableExpansionCore(persona_info)
    if send_msg.is_debug_mode:
        send_msg.send_debug_mode()
    else:
        response = await variable_expansion_core.expand_variable(text=msg)
        if response.code == 200:
            await send_msg.send_render(response.text)
        else:
            await send_msg.send_response_check_code(response, "Error: VariableExpansion")
