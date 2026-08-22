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
        "NoPromptEcho",
        "NO_PROMPT_ECHO"
    }
    cmd_type = CmdTypes.ECHO
    description = f"""
    Echo a message.
    If not arguments, echo the last message.

    Usage:
      /{cmd} [message]
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if not persona_info:
            new_message = await CommandCaller.wait_message(persona_info.namespace)
            message = new_message.message
        else:
            message =  persona_info.message
        await send_msg.send_any(message, reply = False)