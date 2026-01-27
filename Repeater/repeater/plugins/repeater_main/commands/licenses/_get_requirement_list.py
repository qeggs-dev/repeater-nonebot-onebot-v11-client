from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Message
from nonebot.adapters import Bot

from ...assist import PersonaInfo, SendMsg
from .._clients import LicenseCore

get_requirement_list = on_command("getRequirementList", aliases={"grls", "get_requirement_list", "Get_Requirement_List", "GetRequirementList"}, rule=to_me(), block=True)

@get_requirement_list.handle()
async def handle_get_requirement_list(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)
    send_msg = SendMsg("Licenses.Get_Requirement_List", get_requirement_list, persona_info)
    version_core = LicenseCore()

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        server_requirements = await version_core.get_requirement_list()
        version_data = server_requirements.get_data()
        if not version_data:
            await send_msg.send_error("Server requirements data is invalid.")
        else:
            text_buffer: list[str] = []
            for index, requirement in enumerate(version_data, start = 1):
                text_buffer.append(f"{index}. {requirement}")
            await send_msg.send_check_length("\n".join(text_buffer))