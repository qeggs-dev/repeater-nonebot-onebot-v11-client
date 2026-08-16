import json
import yaml

from enum import StrEnum

from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig, OperationType


class FormatType(StrEnum):
    JSON = "json"
    YAML = "yaml"


@CommandCaller.register
class GetConfigs(BaseConfig):
    cmd = "getConfigs"
    aliases = {
        "gcfg",
        "GCFG",
        "get_configs",
        "Get_Configs",
        "GetConfigs",
        "GET_CONFIGS"
    }
    operation = OperationType.GET

    async def parse_value(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
        raw_value: FormatType | None,
    )  -> FormatType:
        msg = persona_info.message_stripped_str.strip()
        if not msg:
            return FormatType.JSON  # default to JSON
        try:
            format_type = FormatType(msg.lower())
        except ValueError:
            await send_msg.send_error("Format type is not supported. Please use 'json' or 'yaml'.")
        return format_type
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: FormatType
        ):
        if response:
            try:
                data = response.json()
                match value:
                    case FormatType.JSON:
                        await send_msg.send_render_prompt(
                            "``` json\n" +
                            json.dumps(data, ensure_ascii=False, indent=4) + 
                            "\n```"
                        )
                    case FormatType.YAML:
                        await send_msg.send_render_prompt(
                            "``` yaml\n" +
                            yaml.safe_dump(data, allow_unicode=True) +
                            "\n```"
                        )
            except (json.JSONDecodeError, yaml.YAMLError, TypeError) as e:
                await send_msg.send_error(f"Failed to format configs: {e}")
        else:
            error_msg = "Failed to get configs."
            error_response = response.get_error() if response else None
            if error_response:
                await send_msg.send_error_response(error_response)
            await send_msg.send_error(error_msg)