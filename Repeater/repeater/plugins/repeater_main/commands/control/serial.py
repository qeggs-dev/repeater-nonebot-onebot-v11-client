from typing import Any, Type
from nonebot.adapters.onebot.v11 import Message
from ...assist import PersonaInfo, SendMsg, Variables
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ._parse_input import parse_input
from ._split_by_indent import split_by_indent
from ._fill_var import fill_var

@CommandCaller.register
class Serial(CommandPackage):
    cmd = "serial"
    aliases = {
        "ser",
        "SER",
        "Serial",
        "SERIAL",
    }
    cmd_type = CmdTypes.CONTROL
    description = f"""
        Execute Commands Serially

        Usage:
        ```
        /{cmd}
        /cmd1_trigger cmd1_args...
        /cmd2_trigger
            cmd2_args1
            cmd2_args
            ...
        /cmd3_trigger cmd3_args...
        ...
        ```
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        lines = split_by_indent(persona_info.message)
        try:
            command_call: list[tuple[Type[CommandPackage[Any]], Message]] = parse_input(lines)
        except ValueError as e:
            await send_msg.send_error(f"Invalid Input Format: {e}")
        except KeyError as e:
            await send_msg.send_error(f"Unknown Command: {e}")
        
        tasks: list[tuple[CommandPackage[Any], PersonaInfo, SendMsg]] = []
        for index, (package, args) in enumerate(command_call):
            try:
                package_instance = CommandCaller.get_instance(package)
            except KeyError:
                await send_msg.send_error(f"[{index}] Handler instance not found")
                send_msg.break_handler()
            copyed_persona_info = persona_info.copy_with_args(args)
            copyed_send_msg = send_msg.copy(
                component = package_instance.component
            )
            tasks.append(
                (
                    package_instance,
                    copyed_persona_info,
                    copyed_send_msg
                )
            )

        user_variables = CommandCaller.variables.setdefault(persona_info.namespace, Variables())
        results = []
        for package, info, send_msg in tasks:
            result = await CommandCaller.horizontal_call(
                package,
                fill_var(info, user_variables),
                send_msg
            )
            results.append(result)