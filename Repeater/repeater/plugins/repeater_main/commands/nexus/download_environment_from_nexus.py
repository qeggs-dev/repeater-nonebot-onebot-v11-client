from .._bases.base_nexus import DownloadFromNexus
from ...command_register import CommandCaller
from ...clients import NexusClient
from ...assist import PersonaInfo

@CommandCaller.register
class EnvDownloadFromNexus(DownloadFromNexus):
    cmd = "envDownloadFromNexus"
    aliases = {
        "edfn",
        "EDFN",
        "env_download_from_nexus",
        "Env_Download_From_Nexus",
        "EnvDownloadFromNexus",
        "ENV_DOWNLOAD_FROM_NEXUS",
    }

    async def get_client(self, persona_info: PersonaInfo):
        user_configs = await persona_info.get_user_configs()
        return NexusClient(persona_info, user_configs)