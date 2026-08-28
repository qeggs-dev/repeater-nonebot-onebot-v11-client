import random
import hashlib
from datetime import datetime
from typing import Literal
from ...assist import PersonaInfo, SendMsg, Namespace
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)

@CommandCaller.register
class RandomFortune(CommandPackage):
    cmd = "randomFortune"
    aliases = {
        "rf",
        "RF",
        "random_fortune",
        "Random_Fortune",
        "RandomFortune",
        "RANDOM_FORTUNE"
    }
    cmd_type = CmdTypes.GAMES
    description = f"""
        Randomly generate daily fortunes.

        Usage:
        ```
        /{cmd} [@someone]...
        ```
    """

    @staticmethod
    def daily_seed(time: datetime) -> int:
        return time.year ^ time.month ^ time.day
    
    @staticmethod
    def int_to_bytes(n: int, byteorder: Literal["big", "little"] = "big", signed: bool = False) -> bytes:
        length = (n.bit_length() + 7) // 8
        if signed and n < 0:
            length = (n.bit_length() + 8) // 8
        return n.to_bytes(length, byteorder, signed=signed)
    
    @classmethod
    def see_fortune(cls, now: datetime, user_ids: list[str]):
        daily_seed = cls.daily_seed(now)
        hash_value = hashlib.pbkdf2_hmac(
            hash_name = "sha256",
            password = cls.int_to_bytes(daily_seed),
            salt = ("\n".join(user_ids)).encode("utf-8"),
            iterations = 10 ** 5
        )
        seed = int.from_bytes(hash_value, "big")
        rand = random.Random(seed)
        fortunes: dict[str, float] = {
            "Money": rand.random(),
            "Love": rand.random(),
            "Work": rand.random(),
            "Health": rand.random(),
            "Social": rand.random(),
            "Study": rand.random(),
            "Travel": rand.random(),
        }
        average = sum(fortunes.values()) / len(fortunes)
        text_buffer = [f"{key} Fortune: {value:.2%}" for key, value in fortunes.items()]
        extreme_luck_factor = ((average-0.5)**2) / 0.25
        return (
            f"Extreme Luck Factor: {extreme_luck_factor:.2%}\n"
            f"Average Fortune: {average:.2%}\n" +
            "\n".join(text_buffer)
        )
        
    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        now = datetime.now()
        at_list = persona_info.noself_at_list
        user_ids = [persona_info.user_id] + at_list
        
        fortune_text = self.see_fortune(now, user_ids)
        await send_msg.send_prompt(fortune_text)