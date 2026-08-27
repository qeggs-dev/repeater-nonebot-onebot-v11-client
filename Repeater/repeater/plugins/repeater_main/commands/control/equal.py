from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from .serial import Serial

@CommandCaller.register
class Equal(CommandPackage):
    cmd = "equal"
    aliases = {
        "eq",
        "EQ",
        "Equal",
        "EQUAL",
    }
    cmd_type = CmdTypes.CONTROL
    description = f"""
    Determines whether multiple messages are equal after removing leading and trailing space characters
    One message per line, the label must be exclusive to the entire line
    If they are equal, serial is called to execute the part after "true:"
    If one is not equal or there are no messages, serial is called to execute the section after "false:"

    Usage: 
        /{cmd}
        message1
        message2
        true:
          ...
        false:
          ...
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        lines = persona_info.message_cqcode.splitlines()

        messages: list[str] = []
        true_code: list[str] = []
        false_code: list[str] = []
        
        now_code: bool | None = None
        for line in lines:
            match line:
                case "true:":
                    now_code = True
                case "false:":
                    now_code = False
                case _:
                    if now_code is None:
                        messages.append(
                            line.strip()
                        )
                    elif now_code:
                        true_code.append(
                            line.removeprefix(" " * 2)
                        )
                    else:
                        false_code.append(
                            line.removeprefix(" " * 2)
                        )

        if len(messages) == 2:
            result = messages[0] == messages[1]
        elif messages:
            first_message = messages[0]
            result = any(
                first_message == message
                for message in messages[1:]
            )
        else:
            result = False

        if result:
            code = true_code
        else:
            code = false_code

        execable_code = persona_info.make_message(
            "\n".join(code)
        )

        await CommandCaller.horizontal_call(
            package = Serial,
            persona_info = persona_info.copy_with_args(
                args = execable_code
            ),
            send_msg = send_msg,
        )
