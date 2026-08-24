from ...command_register import(
    CommandPackage,
    CommandCaller
)
from ...assist import SendMsg
from ...cmd_info import CmdTypes
from typing import Iterable, NoReturn, Generator

def all_joined_commands(cmd: tuple[str, ...], delimiters: Iterable[str]) -> Generator[str, None, None]:
    return (delimiter.join(cmd) for delimiter in delimiters)

def all_splited_commands(cmd: str, delimiters: Iterable[str]) -> Generator[tuple[str, ...], None, None]:
    return (tuple(cmd.split(delimiter)) for delimiter in delimiters)

async def see_cmds(
        commands: dict[CmdTypes, list[CommandPackage]],
        delimiters: set[str],
        send_msg: SendMsg
    ) -> NoReturn:
    text_buffers: list[str] = []
    for cmd_type in commands:
        text_buffer: list[str] = []
        text_buffer.append(f"### Repeater.{cmd_type.value}")
        for package in commands[cmd_type]:
            text_buffer.append("")
            text_buffer.append(f"**{package.component}**")
            text_buffer.append(f"**type**: `{cmd_type.value}`")
            text_buffer.append(f"**Superuser permissions required**: `{package.superuser_permissions}`")
            if package.description:
                text_buffer.append("")
                text_buffer.append(package.get_description().replace("\n", "\n> "))
                text_buffer.append("")
            
            text_buffer.append("**trigger:**")
            if isinstance(package.cmd, str):
                text_buffer.append(f"  - **cmd:** {package.cmd}")
            elif isinstance(package.cmd, tuple):
                text_buffer.append("  - **cmd:**")
                for cmd in all_joined_commands(package.cmd, delimiters):
                    text_buffer.append(f"    - {cmd}")
            else:
                raise TypeError(f"{package.cmd} is not a valid command")
            
            if package.aliases:
                text_buffer.append("  - **aliases:**")
                for alias in CommandCaller.get_package_aliases(package):
                    if isinstance(alias, str):
                        text_buffer.append(f"    - {alias}")
                    elif isinstance(alias, tuple):
                        for sub_alias in all_joined_commands(alias, delimiters):
                            text_buffer.append(f"    - {sub_alias}")
                    else:
                        raise TypeError(f"{alias} is not a valid alias")
        text = "\n".join(text_buffer)
        if text:
            text_buffers.append(text)
    
    text = "\n\n---\n\n".join(text_buffers)
    if not text:
        await send_msg.send_error("Text Buffer is Empty")
    await send_msg.send_render_prompt(text)
    send_msg.break_handler()