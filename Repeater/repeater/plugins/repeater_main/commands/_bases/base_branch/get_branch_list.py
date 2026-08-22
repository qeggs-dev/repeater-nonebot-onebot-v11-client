import re

from ....assist import PersonaInfo, SendMsg
from .base_branch import BaseBranch

class GetBranchList(BaseBranch):

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        try:
            pattern = re.compile(persona_info.message_stripped_str)
        except re.error:
            await send_msg.send_error("Invalid regex pattern.")
        
        client = await self.get_client(persona_info)
        response = await client.get_branch_list()
        if response.code == 200:
            data = response.json()
            if not isinstance(data, list):
                await send_msg.send_error("Unable to process data.")

            text_buffer: list[str] = []
            text_buffer.append(f"Branch Type: {self.userdata_cmds_type.value}")
            text_buffer.append(f"User Name: {persona_info.display_name}")
            if data:
                text_buffer.append("Branchs:")
                for branch_id in data:
                    if pattern.match(branch_id):
                        text_buffer.append(f"  - {branch_id}")
            else:
                text_buffer.append("No branchs found.")

            await send_msg.send_check_length_prompt("\n".join(text_buffer))
        else:
            await send_msg.send_response_check_code(response, f"Get {self.userdata_cmds_type.name} branch list failed")