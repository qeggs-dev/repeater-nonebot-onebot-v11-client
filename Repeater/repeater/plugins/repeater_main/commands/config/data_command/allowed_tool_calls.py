import json
from ....assist import PersonaInfo, SendMsg, Response, parse_delimited_string
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig
from typing import Any

@CommandCaller.register
class AllowedToolCalls(BaseConfig):
    cmd = "allowedToolCalls"
    aliases= {
        "atc",
        "ATC",
        "allowed_tool_calls",
        "Allowed_Tool_Calls",
        "AllowedToolCalls",
        "ALLOWED_TOOL_CALLS",
    }
    field = "allowed_tool_calls"

    async def parse_value(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
        raw_value: Any | None = None
    ) -> list[str] | None:
        msg = persona_info.message_stripped_str
        value = parse_delimited_string(msg)
        if not value:
            return None
        return value
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: list[str] | None
        ):
        if value is None:
            await send_msg.send_response_check_code(response, f"Reset Allowed Tool Calls")
        else:
            await send_msg.send_response_check_code(response, f"Set Allowed Tool Calls to {json.dumps(value, ensure_ascii = False)}")