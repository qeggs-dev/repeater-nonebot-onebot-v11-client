import re

from ...assist import PersonaInfo, SendMsg, SendingTarget
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)

@CommandCaller.register
class Silence(CommandPackage):
    cmd = "silence"
    aliases = {
        "sil",
        "SIL",
        "Silence",
        "SILENCE"
    }
    cmd_type = CmdTypes.CONTROL
    description = f"""
        Executes a command, but discards its output.

        Usage:
        ```
        /{cmd} command [args]
        ```
    """

    pattern = re.compile(r"^(?P<command>[/\w\.]+)\s*(?P<args>.*)$", re.IGNORECASE | re.DOTALL | re.UNICODE)

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        msg = str(persona_info.message)
        
        matched = self.pattern.match(msg)
        if matched:
            command = matched.group("command")
            args_prefix = matched.group("args")

            assert isinstance(command, str), "command must be str"
            assert isinstance(args_prefix, str), "args_prefix must be str"

            args = persona_info.make_message(args_prefix)

            try:
                package = CommandCaller.match_trigger_or_component(command)
            except KeyError:
                await send_msg.send_error(f"Command {command} not found")
                return
            
            try:
                package_instance = CommandCaller.get_instance(package)
            except KeyError as e:
                await send_msg.send_error(f"Command {command} instance not found: {e}")
                return

            copyed_persona_info = persona_info.copy(
                args = args
            )
            copyed_send_msg = send_msg.copy(
                component = package_instance.component,
                send_target = SendingTarget.NULL
            )
            await CommandCaller.horizontal_call(
                package_instance,
                copyed_persona_info,
                copyed_send_msg
            )
        else:
            await send_msg.send_error("Invalid command format")