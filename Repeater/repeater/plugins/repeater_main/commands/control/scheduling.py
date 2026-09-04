import re

from ...assist import PersonaInfo, SendMsg, SendingTarget
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)

@CommandCaller.register
class Scheduling(CommandPackage):
    cmd = "scheduling"
    aliases = {
        "scdl",
        "SCDL",
        "Scheduling",
        "SCEDULING"
    }
    cmd_type = CmdTypes.CONTROL
    description = f"""
        Create a scheduled task using a cron expression.

        Usage:
        ```
        /{cmd} {{cron_expression}} command [args]
        ```
        PS: The curly braces need to be retained here to ensure that the cron expression resolves properly.
    """

    pattern = re.compile(r"^(?P<cron_expression>\{.*\})\s*(?P<components_or_trigger>[/\w_\.]+)\s*(?P<args>.*)$", re.IGNORECASE | re.DOTALL | re.UNICODE)

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        msg = str(persona_info.message)
        
        matched = self.pattern.match(msg)
        if matched:
            cron = matched.group("cron_expression")
            components_or_trigger = matched.group("components_or_trigger")
            args_prefix = matched.group("args")

            assert isinstance(cron, str), "cron must be str"
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

            copyed_persona_info = persona_info.copy(
                args = args
            )
            copyed_send_msg = send_msg.copy(
                component = package_instance.component
            )
            try:
                await CommandCaller.timed_scheduling(
                    package = package_instance,
                    cron = cron,
                    persona_info = copyed_persona_info,
                    send_msg = copyed_send_msg
                )
            except ValueError as e:
                await send_msg.send_error(f"Cron format error: {e}")
        else:
            await send_msg.send_error("Invalid command format")