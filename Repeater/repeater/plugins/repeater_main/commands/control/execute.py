import re
import asyncio

from typing import Any, Type
from nonebot.adapters.onebot.v11 import Message
from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)

@CommandCaller.register
class Execute(CommandPackage):
    cmd = "execute"
    aliases = {
        "e",
        "E",
        "Execute",
        "EXECUTE"
    }
    cmd_type = CmdTypes.CONTROL
    description = f"""
        Pull Up the command invocation through component when only the component of the command are known.

        Usage:
            /{cmd} component args
    """

    pattern = re.compile(r"^(?P<components>[\w\.]+)\s*(?P<args>.*)$", re.IGNORECASE | re.DOTALL | re.UNICODE)

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        msg = str(persona_info.message)
        
        matched = self.pattern.match(msg)
        if matched:
            components = matched.group("components")
            args_prefix = matched.group("args")

            assert isinstance(components, str), "components must be str"
            assert isinstance(args_prefix, str), "args_prefix must be str"

            args = Message(args_prefix)

            try:
                package = CommandCaller.match_component(components)
            except KeyError:
                await send_msg.send_error(f"Command {components} not found")
                return
            
            try:
                package_instance = CommandCaller.get_instance(package)
            except KeyError as e:
                await send_msg.send_error(f"Command {components} instance not found: {e}")
                return

            copyed_persona_info = persona_info.copy_with_args(
                args = args
            )
            copyed_send_msg = send_msg.copy(
                component = package_instance.component
            )
            await CommandCaller.horizontal_call(
                package_instance,
                copyed_persona_info,
                copyed_send_msg
            )
        else:
            await send_msg.send_error("Invalid command format")