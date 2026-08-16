from ...assist import escape_string
from ...command_register import CommandPackage, CommandCaller
from nonebot.adapters.onebot.v11 import Message
from typing import Type, Any

def parse_input(message: list[list[Message]]) -> list[tuple[type[CommandPackage[Any]], Message]]:
    command_call: list[tuple[Type[CommandPackage[Any]], Message]] = []
    for index, line in enumerate(message, start=1):
        if not line:
            continue

        name: str = ""
        args: Message = Message()
        first_message = line[0]
        text = first_message.extract_plain_text()
        prefix, rest_text = split_cmd_prefix(text)
        if not prefix:
            raise ValueError(f"[{index}] {rest_text} is not a command")
        
        name_buffer: list[str] = []
        for index, char in enumerate(rest_text):
            if char == " ":
                name = "".join(name_buffer)
                rest_text = rest_text[index + 1:]
                break
            name_buffer.append(char)
        else:
            # no break
            if name_buffer:
                name = "".join(name_buffer)
                rest_text = ""

        
        args = Message(rest_text)
        for msg in line[1:]:
            for segment in msg:
                args.append(segment)

        command_call.append(
            (
                CommandCaller.match_trigger(name),
                args
            )
        )

    return command_call

def split_cmd_prefix(name: str) -> tuple[str, str]:
    for prefix in CommandCaller.cmd_prefixs():
        if name.startswith(prefix):
            return prefix, name.removeprefix(prefix)

    return "", name