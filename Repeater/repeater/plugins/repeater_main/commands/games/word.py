from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from nonebot.adapters.onebot.v11 import Message


@CommandCaller.register
class Word(CommandPackage):
    cmd = "word"
    aliases = {
        "Word",
        "WORD"
    }
    cmd_type = CmdTypes.GAMES
    description = f"""
        Write a sentence, or get the last person's sentence.

        Usage:
        ```
        /{cmd} <sentence>
        ```
    """
    def __post_init__(self):
        self.word: Message | None = None

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if persona_info:
            self.word = persona_info.message
            await send_msg.send_prompt("Got it!")
        elif self.word:
            await send_msg.send_any(self.word, reply = False)
        else:
            await send_msg.send_error("Please write a sentence.")