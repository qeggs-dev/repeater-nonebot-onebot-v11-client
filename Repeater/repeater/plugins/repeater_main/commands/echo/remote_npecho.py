import re
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from nonebot.adapters.onebot.v11 import Message
from ...cmd_info import CmdTypes
from ...assist import PersonaInfo, SendMsg, SendingTarget

@CommandCaller.register
class RemoteNoPromptEcho(CommandPackage):
    cmd = "remoteNoPromptEcho"
    aliases = {
        "rnpecho",
        "RNPECHO",
        "remote_no_prompt_echo",
        "Remote_No_Prompt_Echo",
        "RemoteNoPromptEcho",
        "REMOTE_NO_PROMPT_ECHO"
    }
    cmd_type = CmdTypes.ECHO
    description = f"""
        Send the message somewhere else and no prompt.
        
        Usage:
        ```
        /{cmd} group:<group_id> <message>
        /{cmd} private:<user_id> <message>
        ```
    """

    pattern = re.compile(r"^(?P<mode>group|private)\s*:\s*(?P<id>\d+)\s*(?P<message>.+)$")

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        match = self.pattern.match(str(persona_info.message))
        if match:
            mode = match.group("mode")
            id = match.group("id")
            message_str = match.group("message")
            message = Message(message_str)
            match mode:
                case "group":
                    remote_send_msg = send_msg.copy(
                        target_group = id,
                        send_target = SendingTarget.API,
                    )
                case "private":
                    remote_send_msg = send_msg.copy(
                        target_user = id,
                        send_target = SendingTarget.API,
                    )
                case _:
                    await send_msg.send_prompt("Invalid mode, only 'group' or 'private' is allowed.")
                    send_msg.break_handler()
            remote_message = persona_info.copy_with_args(
                args = message,
            )
            if not remote_message:
                new_message = await CommandCaller.wait_message(persona_info.namespace)
                await remote_send_msg.send_any(new_message.message, reply = False)
            else:
                await remote_send_msg.send_any(remote_message.message, reply = False)
        else:
            await send_msg.send_prompt("Invalid format, please use 'group:<id> <message>' or 'private:<id> <message>'.")
            return