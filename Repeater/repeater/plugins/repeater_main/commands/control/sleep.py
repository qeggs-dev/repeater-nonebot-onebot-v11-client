import asyncio

from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)

@CommandCaller.register
class Sleep(CommandPackage):
    cmd = "sleep"
    aliases = {
        "s",
        "S",
        "Sleep",
        "SLEEP",
    }
    cmd_type = CmdTypes.CONTROL
    description = f"""
    Sleep for a specified number of seconds

    Usage: 
        /{cmd} seconds
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        try:
            sleep_time = float(persona_info.message_stripped_str)
        except ValueError:
            await send_msg.send_error("Please enter a valid number")
            return
        
        if sleep_time < 0:
            await send_msg.send_error("Please enter a positive number")
            return
        
        await asyncio.sleep(sleep_time)