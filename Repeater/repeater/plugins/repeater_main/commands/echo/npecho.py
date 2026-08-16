from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...cmd_info import CmdTypes
from ...assist import PersonaInfo, SendMsg

@CommandCaller.register
class NPEcho(CommandPackage):
    cmd = "noPromptEcho"
    aliases = {
        "npecho",
        "NPECHO",
        "no_prompt_echo",
        "No_Prompt_Echo",
        "NoPromptEcho"
    }
    cmd_type = CmdTypes.ECHO

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if not persona_info:
            new_message = await CommandCaller.wait_message(persona_info.namespace)
            await send_msg.send_any(new_message.message, reply = False)
        else:
            await send_msg.send_any(persona_info.message, reply = False)