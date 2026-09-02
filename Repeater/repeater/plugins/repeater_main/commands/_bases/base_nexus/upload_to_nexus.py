from .base_nexus import BaseNexus
from ....assist import PersonaInfo, SendMsg

class UploadToNexus(BaseNexus):
    @classmethod
    def documents(cls):
        docs = [
            f"Upload {cls.userdata_cmds_type.value} data to Nexus.",
            "",
            "Usage:",
            "```",
            f"/{cls.cmd}",
            "```"
        ]
        cls.description = "\n".join(docs)
        return cls.description
    
    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        nexus_client = await self.get_client(persona_info)

        timeout = None
        if persona_info.message_stripped_str:
            try:
                timeout = int(persona_info.message_stripped_str)
            except ValueError:
                await send_msg.send_error("Invalid timeout value")

        response = await nexus_client.upload_to_nexus(timeout)

        if response:
            data = response.get_data()
            if data is None:
                await send_msg.send_error("Unable to process data.")
            else:
                await send_msg.send_prompt(
                    f"Upload successful.\nFile ID: {data.resource_uuid}"
                )
        else:
            await send_msg.send_response_check_code(response, "Unable to upload to Nexus.")