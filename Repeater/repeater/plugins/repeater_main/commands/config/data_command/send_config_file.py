from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig, OperationType

@CommandCaller.register
class SendConfigFile(BaseConfig):
    cmd = "sendConfigFile"
    aliases = {
        "scfgf",
        "SCFGF",
        "send_config_file",
        "Send_Config_File",
        "SendConfigFile",
        "SCFGF"
    }
    operation = OperationType.GET_FILE_URL
    description = f"""
    Export the configuration file.

    Usage:
      /{cmd}
    """

    async def parse_value(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
        raw_value: None,
    )  -> None:
        return None
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: None
        ):
        if value:
            await send_msg.send_file(value, f"{persona_info.namespace_str}_User_Config.json")
        else:
            await send_msg.send_error("Failed to get config file URL")