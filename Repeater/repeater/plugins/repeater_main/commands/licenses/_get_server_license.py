from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Message
from nonebot.adapters import Bot

from ...assist import PersonaInfo, SendMsg
from .._clients import LicenseCore

get_server_licenses = on_command("getServerLicenses", aliases={"gsl", "get_server_licenses", "Get_Server_License", "GetServerLicense"}, rule=to_me(), block=True)

@get_server_licenses.handle()
async def handle_get_server_licenses(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)
    send_msg = SendMsg("Licenses.Get_Server_License", get_server_licenses, persona_info)
    version_core = LicenseCore()

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        server_version = await version_core.get_server_licenses()
        version_data = server_version.get_data()
        if version_data is None:
            await send_msg.send_error("Server License Data is Invalid.")
        message = Message()
        for name, license in version_data.items():
            message.append(MessageSegment.text(f"{name}:\n"))
            message.append(await send_msg.text_render(license))
        await send_msg.send_prompt(message)