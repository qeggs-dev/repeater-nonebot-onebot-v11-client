from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...client_configs import storage_configs


@CommandCaller.register
class Ciallo(CommandPackage):
    cmd = "ciallo"
    aliases = {
        "Ciallo",
        "CIALLO"
    }
    cmd_type = CmdTypes.GAMES
    description = f"""
        Ciallo~ (∠・ω< )⌒★

        Usage:
        ```
        /{cmd}
        ```
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        await send_msg.send_text(storage_configs.ciallo_content)