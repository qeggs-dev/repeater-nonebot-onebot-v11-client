import json
from ....assist import PersonaInfo, SendMsg, Response, parse_delimited_string
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig, OperationType

@CommandCaller.register
class DisallowTools(BaseConfig):
    cmd = "disallowTools"
    aliases= {
        "dt",
        "DT",
        "disallow_tools",
        "Disallow_Tools",
        "DisallowTools",
        "DISALLOW_TOOLS",
    }
    field = "allowed_tool_calls"
    operation = OperationType.GET_AND_SET

    async def parse_value(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
        raw_value: list[str] | None = None
    ):
        disable_tools = set(parse_delimited_string(persona_info.message_stripped_str))
        disabled_tools: list[str] = []
        for tool in raw_value or []:
            if tool not in disable_tools:
                disabled_tools.append(tool)
        return disabled_tools
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: list[str] | None
        ):
            await send_msg.send_response_check_code(response, f"Set Tool Calls to {json.dumps(value, ensure_ascii = False)}")