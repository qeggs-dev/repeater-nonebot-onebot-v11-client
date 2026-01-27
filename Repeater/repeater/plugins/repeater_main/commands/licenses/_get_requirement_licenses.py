from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Message
from nonebot.adapters import Bot

from ...assist import PersonaInfo, SendMsg
from .._clients import LicenseCore

get_requirement_licenses = on_command("getRequirementLicenses", aliases={"grl", "get_requirement_license", "Get_Requirement_License", "GetRequirementLicense"}, rule=to_me(), block=True)

@get_requirement_licenses.handle()
async def handle_get_requirement_license(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)
    send_msg = SendMsg("Licenses.Get_Requirement_License", get_requirement_licenses, persona_info)
    version_core = LicenseCore()

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        server_version = await version_core.get_requirement_license(persona_info.message_str)
        version_data = server_version.get_data()
        if version_data is None:
            await send_msg.send_error("Server license data is invalid.")
        message = Message()
        for name, license in version_data.items():
            message.append(MessageSegment.text(f"{name}:\n"))
            message.append(await send_msg.text_render(license, direct_output = True))
        await send_msg.send_prompt(message)