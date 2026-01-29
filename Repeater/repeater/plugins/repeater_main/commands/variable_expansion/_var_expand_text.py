from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .._clients import VariableExpansionCore
from ...assist import PersonaInfo, SendMsg

var_expand_text = on_command("varExpandText", aliases={"vet", "var_expand_text", "Var_Expand_Text", "VarExpandText"}, rule=to_me(), block=True)

@var_expand_text.handle()
async def handle_var_expand_text(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("VarExpandText", var_expand_text, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    msg = args.extract_plain_text().strip()

    variable_expansion_core = VariableExpansionCore(persona_info)
    response = await variable_expansion_core.expand_variable(text=msg)
    if response.code == 200:
        await send_msg.send_text(response.text)
    else:
        await send_msg.send_response_check_code(response, "Error: VariableExpansion")
