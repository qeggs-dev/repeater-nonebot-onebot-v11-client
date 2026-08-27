import re
import asyncio

from typing import Any, Type
from nonebot.adapters.onebot.v11 import MessageSegment
from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ._remove_cmd_prefix import remove_cmd_prefix

@CommandCaller.register
class Loop(CommandPackage):
    cmd = "loop"
    aliases = {
        "l",
        "L",
        "Loop",
        "LOOP"
    }
    cmd_type = CmdTypes.CONTROL
    description = f"""
        loop execute command times

        Usage:
            /{cmd} times command [args]
    """

    pattern = re.compile(r"^(?P<times>\d*)\s*(?P<command>[/\w_\.]+)\s*(?P<args>.*)$", re.IGNORECASE | re.DOTALL | re.UNICODE)

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        matched = self.pattern.match(persona_info.message_cqcode)
        if matched:
            times_str = matched.group("times")
            command = matched.group("command")
            args_str = matched.group("args")

            assert isinstance(times_str, str), "times_str must be str"
            assert isinstance(command, str), "command must be str"
            assert isinstance(args_str, str), "args_str must be str"

            args = persona_info.make_message(args_str)

            if not times_str:
                times = 1
            else:
                times = int(times_str)
            
            if times < 1:
                await send_msg.send_error("times must be greater than 0")
                return

            try:
                package = CommandCaller.match_trigger_or_component(command)
            except KeyError:
                await send_msg.send_error(f"Command {command} not found")
                return
            
            try:
                package_instance = CommandCaller.get_instance(package)
            except KeyError as e:
                await send_msg.send_error(f"Command instance {command} not found: {e}")
                return

            copyed_persona_info = persona_info.copy_with_args(
                args = args
            )
            copyed_send_msg = send_msg.copy(
                component = package_instance.component
            )
            for i in range(times):
                await CommandCaller.horizontal_call(
                    package_instance,
                    copyed_persona_info,
                    copyed_send_msg
                )
        else:
            await send_msg.send_error("Invalid command format")