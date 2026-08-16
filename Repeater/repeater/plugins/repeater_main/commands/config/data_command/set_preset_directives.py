import json
from ....assist import PersonaInfo, SendMsg, Response, parse_delimited_string
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig
from typing import Any
from pydantic import BaseModel, ValidationError

@CommandCaller.register
class SetPresetDirectives(BaseConfig):
    cmd = "setPresetDirectives"
    aliases= {
        "spd",
        "SPD",
        "set_preset_directives",
        "Set_Preset_Directives",
        "SetPresetDirectives",
        "SET_PRESET_DIRECTIVES",
    }
    field = "prompt_directives"

    class Input(BaseModel):
        preset_directives: dict[str, list[str]]

    async def parse_value(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
        raw_value: Any | None = None
    ) -> dict[str, list[str]] | None:
        msg = persona_info.message_stripped_str
        data = json.loads(msg)
        try:
            input_data = self.Input(preset_directives=data)
        except ValidationError as e:
            errors = e.errors()
            buffer: list[str] = []
            for error in errors:
                buffer.append(error["msg"])
            await send_msg.send_error("\n".join(buffer))
        
        return input_data.preset_directives
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: dict[str, list[str]] | None
        ):
        if value is None:
            await send_msg.send_response_check_code(response, f"Reset Preset Directives")
        else:
            await send_msg.send_response_check_code(response, f"Set Preset Directives to {json.dumps(value, ensure_ascii = False)}")