import re

from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)

@CommandCaller.register
class Bypass(CommandPackage):
    cmd = "bypass"
    aliases = {
        "byp",
        "BYP",
        "Bypass",
        "BYPASS"
    }
    cmd_type = CmdTypes.CONTROL
    description = f"""
        Run a command in the background,
        and quits immediately.

        Usage:
        ```
        /{cmd} command [args]
        ```
    """

    pattern = re.compile(r"^(?P<components_or_trigger>[/\w_\.]+)\s*(?P<args>.*)$", re.IGNORECASE | re.DOTALL | re.UNICODE)

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        msg = str(persona_info.message)
        
        matched = self.pattern.match(msg)
        if matched:
            components_or_trigger = matched.group("components_or_trigger")
            args_prefix = matched.group("args")

            assert isinstance(components_or_trigger, str), "components must be str"
            assert isinstance(args_prefix, str), "args_prefix must be str"

            args = persona_info.make_message(args_prefix)

            try:
                package = CommandCaller.match_trigger_or_component(components_or_trigger)
            except KeyError:
                await send_msg.send_error(f"Command {components_or_trigger} not found")
                return
            
            try:
                package_instance = CommandCaller.get_instance(package)
            except KeyError as e:
                await send_msg.send_error(f"Command instance {package.component} not found: {e}")
                return

            copyed_persona_info = persona_info.copy_with_args(
                args = args
            )
            copyed_send_msg = send_msg.copy(
                component = package_instance.component
            )
            await CommandCaller.horizontal_enter_wait_created(
                package_instance,
                copyed_persona_info,
                copyed_send_msg
            )
        else:
            await send_msg.send_error("Invalid command format")