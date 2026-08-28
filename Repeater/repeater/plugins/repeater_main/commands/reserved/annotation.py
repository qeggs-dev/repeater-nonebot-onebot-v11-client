from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...cmd_info import CmdTypes

@CommandCaller.register
class Annotation(CommandPackage):
    cmd = "#"
    aliases = {
        "/",
        "anot",
        "ANOT",
        "annotation",
        "Annotation",
        "ANNOTATION",
    }
    cmd_type = CmdTypes.RESERVED
    description = """
    Null command, which can be used for comments.

    Usage:
    ```
    /#
    //
    ```
    """
    empty_handler = True

    async def handler(self, persona_info, send_msg):
        pass