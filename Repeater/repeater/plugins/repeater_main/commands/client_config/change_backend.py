from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...client_configs import storage_configs


@CommandCaller.register
class ChangeBackend(CommandPackage):
    cmd = "changeBackend"
    aliases = {
        "cb",
        "CB",
        "change_backend",
        "Change_Backend",
        "ChangeBackend",
        "CHANGE_BACKEND",
    }
    description = f"""
        Let the connector switch the available backends.

        Usage:
        ```
        /{cmd} backend_name
        ```
    """
    cmd_type = CmdTypes.CLIENT_CONFIG

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        user_configs = await persona_info.get_user_configs()
        raw_backend = user_configs.backend
        if raw_backend is None:
            raw_backend = storage_configs.default_backend
        user_configs.backend = persona_info.message_stripped_str
        await persona_info.set_user_configs(user_configs)

        await send_msg.send_prompt(
            f"Change backend {raw_backend} -> {user_configs.backend}"
        )