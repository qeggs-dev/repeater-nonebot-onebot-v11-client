import random
from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...client_configs import storage_configs

@CommandCaller.register
class UselessButton(CommandPackage):
    cmd = "uselessButton"
    aliases = {
        "ub",
        "UB",
        "useless_button",
        "Useless_Button",
        "UselessButton",
        "USELESS_BUTTON"
    }
    cmd_type = CmdTypes.GAMES
    documents = f"""
        A useless button.

        Usage:
        ```
        /{cmd} [times]
        ```
    """

    @staticmethod
    def button():
        button_hit = (random.randint(1, 100) == 25)
        if button_hit:
            useless_button_words = storage_configs.useless_button_words
            weights = [0.5**i for i in range(len(useless_button_words))]
            word = random.choices(storage_configs.useless_button_words, weights)
            if word:
                return word[0]
            else:
                return storage_configs.useless_button_missing
        else:
            return storage_configs.useless_button_missing
    
    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        msg = persona_info.message_stripped_str
        try:
            times = int(msg)
        except ValueError:
            times = 1
        
        if times == 1:
            results = [self.button()]
        elif times > 10:
            await send_msg.send_error("The number of times cannot be greater than 10.")
        elif times > 1:
            results = [f"{i}. {self.button()}" for i in range(1, times + 1)]
        else:
            await send_msg.send_error("The number of times cannot be less than 1.")

        await send_msg.send_check_length("\n".join(results))