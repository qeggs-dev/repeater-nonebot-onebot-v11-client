from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...cmd_info import CmdTypes
from ...assist import PersonaInfo, SendMsg

@CommandCaller.register
class RemoveReply(CommandPackage):
    cmd = "removeReply"
    aliases = {
        "rr",
        "RR",
        "remove_reply",
        "Remove_Reply",
        "RemoveReply",
        "REMOVE_REPLY"
    }
    cmd_type = CmdTypes.ECHO
    description = f"""
    Echo a message.
    If not arguments, echo the last message.

    Usage:
    ```
    /{cmd} [message]
    ```
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if not persona_info:
            new_message = await CommandCaller.wait_message(persona_info.namespace)
            message = new_message.message
        else:
            message =  persona_info.message

        if message and message[0].type == "reply":
            reply_count: int = 0
            for i in range(len(message)):
                if message[i].type == "reply":
                    reply_count += 1

            message = message[reply_count:]

        await send_msg.send_any(message, reply = False)