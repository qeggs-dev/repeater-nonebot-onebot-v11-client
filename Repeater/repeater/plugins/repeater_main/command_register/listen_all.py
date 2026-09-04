import asyncio
from .package import CommandPackage
from .listen_type import ListenType
from .caller import CommandCaller
from ..cmd_info import CmdTypes
from ..assist import PersonaInfo, SendMsg, SendingTarget

@CommandCaller.register
class FrameworkMessageListener(CommandPackage):
    rule = None
    listen_type = ListenType.Message
    cmd_type = CmdTypes.LISTEN_ALL
    priority = 0
    block = False
    document = """
    A Handler inside the Repeater framework for unfiltered message listening.
    """

    async def enter_check(self, persona_info: PersonaInfo, send_msg: SendMsg) -> bool:
        return True

    async def enter_handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        send_msg.sending_target = SendingTarget.NULL
        return await super().enter_handler(persona_info, send_msg)

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        await CommandCaller.report_message(
            persona_info = persona_info
        )