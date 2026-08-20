import asyncio

from typing import Any, Type
from nonebot.adapters.onebot.v11 import Message
from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ._parse_input import parse_input
from ._split_by_indent import split_by_indent

@CommandCaller.register
class Parallel(CommandPackage):
    cmd = "parallel"
    aliases = {
        "par",
        "PAR",
        "Parallel",
        "PARALLEL",
    }
    cmd_type = CmdTypes.CONTROL
    description = f"""
        Execute Commands Parallelly

        Usage:
            /{cmd}
            /cmd1_trigger cmd1_args...
            /cmd2_trigger cmd2_args...
            ...
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        lines = split_by_indent(persona_info.message)
        try:
            command_call: list[tuple[Type[CommandPackage[Any]], Message]] = parse_input(lines)
        except ValueError as e:
            await send_msg.send_error(f"Invalid Input Format: {e}")
        except KeyError as e:
            await send_msg.send_error(f"Unknown Command: {e}")
        
        tasks: list[asyncio.Task[Any]] = []
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
                asyncio.create_task(
                    CommandCaller.horizontal_call(
                        package_instance,
                        persona_info = copyed_persona_info,
                        send_msg = copyed_send_msg
                    )
                )
            )
        
        results = await asyncio.gather(*tasks)