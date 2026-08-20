from typing import Any, Type
from nonebot.adapters.onebot.v11 import Message
from ...assist import PersonaInfo, SendMsg, SendingTarget
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ._parse_input import parse_input
from ._split_by_indent import split_by_indent

@CommandCaller.register
class Cascade(CommandPackage):
    cmd = "cascade"
    aliases = {
        "cas",
        "CAS",
        "Cascade",
        "CASCADE",
    }
    cmd_type = CmdTypes.CONTROL
    description = f"""
        Takes the result of the previous command as input to the next command.
        When args exist, use them instead of what was returned by the previous command.
        Use {{message}} to include the output of the previous entry in args,
        if there is no way to pass the previous line, the result is printed directly.

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
        
        tasks: list[tuple[CommandPackage[Any], PersonaInfo]] = []
        for index, (package, args) in enumerate(command_call):
            try:
                package_instance = CommandCaller.get_instance(package)
                copyed_persona_info = persona_info.copy_with_args(args)
                tasks.append((package_instance, copyed_persona_info))
            except KeyError:
                await send_msg.send_error(f"[{index}] Handler instance not found")
                send_msg.break_handler()
        
        last_result: PersonaInfo = persona_info
        for package_instance, info in tasks:
            copyed_send_msg = send_msg.copy(
                component = package_instance.component
            )

            # 如果当前命令无参数且有上一步结果，使用上一步结果
            if info:
                if "{message}" in str(info.message):
                    info = info.copy_with_args(
                        Message(
                            str(info.message).format(
                                message = str(last_result)
                            )
                        )
                    )
            elif not info and last_result:
                info = last_result
            else:
                await copyed_send_msg.send_any(last_result.message)
                continue
            
            copyed_send_msg.sending_target = SendingTarget.BUFFER
            
            await CommandCaller.horizontal_call(
                package_instance,
                info,
                copyed_send_msg
            )
            
            current_result = Message()
            while copyed_send_msg.buffer.qsize() > 0:
                buffer_result, args, kwargs, send_time = await copyed_send_msg.buffer.get()
                if isinstance(buffer_result, Message):
                    current_result.extend(buffer_result)
                else:
                    current_result.append(buffer_result)
            
            last_result = info.copy_with_args(current_result)
        
        if last_result:
            last_result_message = last_result.message
            while last_result_message:
                if last_result_message[0].type == "reply":
                    last_result_message.pop(0)
                else:
                    break
            await send_msg.send_any(last_result_message)