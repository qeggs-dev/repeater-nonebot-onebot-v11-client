from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ..._clients import ContextCore
from ....assist import PersonaInfo, SendMsg

check_role_structure = on_command("checkRoleStructure", aliases={"crs", "check_role_structure", "Check_Role_Structure", "CheckRoleStructure"}, rule=to_me(), block=True)

@check_role_structure.handle()
async def handle_check_role_structure(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Context.Check_Role_Structure", check_role_structure, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    
    context_core = ContextCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await context_core.check_role_structure()

        if response.code == 200:
            data = response.get_data()
            send_msg.send_prompt(data.message)
        else:
            await send_msg.send_response_check_code(response, "Check Role Structure Failed")