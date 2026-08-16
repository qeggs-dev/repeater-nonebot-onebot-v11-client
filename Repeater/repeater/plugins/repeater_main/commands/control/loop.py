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
    documents = f"""
        loop execute command times

        Usage:
            /{cmd} times command args
    """

    pattern = re.compile(r"^(?P<times>\d*)\s*(?P<command>\S+?)\s*(?P<args>.*)$", re.IGNORECASE | re.DOTALL | re.UNICODE)

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        msg = persona_info.message
        first_segment = msg[0]
        if first_segment.type != "text":
            await send_msg.send_error("Please input a text message.")
        matched = self.pattern.match(first_segment.data["text"])
        if matched:
            times_str = matched.group("times")
            command = matched.group("command")
            args_prefix = matched.group("args")

            assert isinstance(times_str, str), "times_str must be str"
            assert isinstance(command, str), "command must be str"
            assert isinstance(args_prefix, str), "args_prefix must be str"

            command = remove_cmd_prefix(command)

            args = MessageSegment.text(args_prefix) + msg[1:]

            if not times_str:
                times = 1
            else:
                times = int(times_str)
            
            if times < 1:
                await send_msg.send_error("times must be greater than 0")
                return

            try:
                package = CommandCaller.match_trigger(command)
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
            copyed_send_msg = send_msg.copy_with_component(
                package_instance.component
            )
            for i in range(times):
                await CommandCaller.horizontal_call(
                    package_instance,
                    copyed_persona_info,
                    copyed_send_msg
                )
        else:
            await send_msg.send_error("Invalid command format")