from .._bases.base_nexus import UploadToNexus
from ...command_register import CommandCaller
from ...clients import NexusClient
from ...assist import PersonaInfo

@CommandCaller.register
class EnvUploadToNexus(UploadToNexus):
    cmd = "envUploadToNexus"
    aliases = {
        "eutn",
        "EUTN",
        "env_upload_to_nexus",
        "Env_Upload_To_Nexus",
        "EnvUploadToNexus",
        "ENV_UPLOAD_TO_NEXUS",
    }

    async def get_client(self, persona_info: PersonaInfo):
        user_configs = await persona_info.get_user_configs()
        return NexusClient(persona_info, user_configs)