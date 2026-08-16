import random
import asyncio
from typing import Any
from ...assist import PersonaInfo, SendMsg, MessageSource
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)


@CommandCaller.register
class ChooseGroupMember(CommandPackage):
    cmd = "chooseGroupMember"
    aliases = {
        "cgm",
        "CGM",
        "choose_group_member",
        "Choose_Group_Member",
        "ChooseGroupMember",
        "CHOOSE_GROUP_MEMBER",
    }
    cmd_type = CmdTypes.OTHER
    acceptable_sources = {MessageSource.GROUP}

    @staticmethod
    def generate_text(choiced: list[dict[str, Any]]) -> str:
        text_buffer: list[str] = []
        for index, member in enumerate(choiced, start=1):
            nickname = member.get("card")
            if not nickname:
                nickname = member.get("nickname")
            text_buffer.append(f"{index}. {nickname}")
        return "\n".join(text_buffer)

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        group_id = persona_info.group_id

        if not group_id:
            await send_msg.send_error("The current feature cannot be used in private chat.")
        else:
            try:
                n = int(persona_info.message_stripped_str)
            except (ValueError, TypeError):
                await send_msg.send_error("Please enter a number.")

            if n > 0:
                member_list = await persona_info.cached_api.get_group_member_list(
                    group_id = group_id
                )
                if n > len(member_list):
                    await send_msg.send_error(f"The current number is too large, please enter a number less than {len(member_list)}.")
                choiced: list[dict[str, Any]] = random.sample(member_list, n)
                text = await asyncio.to_thread(self.generate_text, choiced)
                await send_msg.send_check_length_prompt(text)
            else:
                await send_msg.send_error("The input must be a positive integer!")