from ...assist import (
    get_first_mentioned_user,
    PersonaInfo,
    Namespace,
    SendMsg
)
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...command_register import CommandCaller, CommandPackage


@CommandCaller.register
class GetNamespace(CommandPackage):
    cmd = "getNamespace"
    aliases = {
        "gns",
        "GNS",
        "get_namespace",
        "Get_Namespace",
        "GetNamespace",
        "GET_NAMESPACE",
    }
    description = f"""
    Get namespace of the group or user.

    Usage:
      /{cmd}
    """
    cmd_type = CmdTypes.NAMESPACE

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        mentioned_id = get_first_mentioned_user(persona_info._message_event)
        group_id = persona_info.group_id
        namespace = persona_info.namespace
        if mentioned_id is None:
            await send_msg.send_prompt(namespace.namespace_str)
        else:
            await send_msg.send_prompt(
                Namespace(
                    mode = namespace.mode,
                    group_id = group_id,
                    user_id = mentioned_id
                ).namespace_str
            )