from ...clients import ChatClient
from ...assist import PersonaInfo
from .._bases import BaseChat
from ...command_register import CommandCaller

@CommandCaller.register
class PublicSpaceChat(BaseChat):
    cmd = "publicSpaceChat"
    aliases = {
        "psc",
        "PSC",
        "public_space_chat",
        "Public_Space_Chat",
        "PublicSpaceChat",
        "Public_Space_Chat"
    }
    description = f"""
        Send a message in public space.
        
        Usage:
        ```
        /{cmd} text
        ```
    """

    async def get_client(self, persona_info: PersonaInfo):
        user_configs = await persona_info.get_user_configs()
        return ChatClient(persona_info, user_configs, persona_info.public_namespace_str)