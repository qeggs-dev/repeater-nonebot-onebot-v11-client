from ...assist import PersonaInfo, SendMsg, MessageSource
from ...command_register import CommandCaller, ListenType
from .._bases import BaseChat
from .smart_at import SmartAt

@CommandCaller.register
class SmartAtCmd(BaseChat):
    cmd = "smartAt"
    aliases = {
        "smat",
        "SMAT",
        "smart_at",
        "Smart_AT",
        "SmartAt",
        "SMARTAT",
    }
    listen_type = ListenType.Command
    description = """
        The command version of SmartAT.

        Usage:
        ```
        @Bot message
        ```

        Or:
        ```
        @Bot
        ```
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        return await CommandCaller.horizontal_call(
            package = SmartAt,
            persona_info = persona_info,
            send_msg = send_msg
        )