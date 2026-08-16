from .base_nexus import BaseNexus
from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes

class DownloadFromNexus(BaseNexus):
    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        nexus_client = await self.get_client(persona_info)
        
        try:
            response = await nexus_client.download_from_nexus(persona_info.message_stripped_str)
        except ValueError as e:
            await send_msg.send_error(
                f"Invalid UUID: {persona_info.message_stripped_str}"
            )

        if response.code == 200:
            data = response.get_data()
            if data is None:
                await send_msg.send_error("Unable to process data.")
            else:
                await send_msg.send_prompt("Download successful.")
        else:
            await send_msg.send_response_check_code(response, "Unable to download from Nexus.")