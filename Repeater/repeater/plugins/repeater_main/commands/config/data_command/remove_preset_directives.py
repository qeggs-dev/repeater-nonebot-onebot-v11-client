import re
import json
from ....assist import PersonaInfo, SendMsg, Response, parse_delimited_string
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig, OperationType

@CommandCaller.register
class RemovePresetDirectives(BaseConfig):
    cmd = "removePresetDirectives"
    aliases= {
        "rpd",
        "RPD",
        "remove_preset_directives",
        "Remove_Preset_Directives",
        "RemovePresetDirectives",
        "REMOVE_PRESET_DIRECTIVES",
    }
    field = "prompt_directives"
    operation = OperationType.GET_AND_SET
    _pattern = re.compile(r"^(?P<name>\S+)\s*:\s*(?P<value>.*)$", re.DOTALL)

    @classmethod
    def parse_input(
        cls,
        text: str
    ):
        match = cls._pattern.match(text)
        if match is None:
            return None
        else:
            name = match.group("name")
            value = match.group("value")
            
            assert isinstance(name, str), "name must be a string"
            assert isinstance(value, str), "value must be a string"

            return {
                name: value
            }

    async def parse_value(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
        raw_value: dict[str, list[str]] | None = None
    ):
        removed_diretives = self.parse_input(persona_info.message_stripped_str)
        if removed_diretives is None:
            await send_msg.send_error("Invalid input format. Expected: <name>: <value>...")

        for type in removed_diretives:
            if type in raw_value:
                diretives = removed_diretives[type]
                for raw_type, raw_directives in raw_value.items():
                    for raw_directive in raw_directives:
                        if raw_directive in diretives:
                            raw_value[raw_type].remove(raw_directive)
        return raw_value
                    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: dict[str, list[str]] | None
        ):
            await send_msg.send_response_check_code(response, f"Removed Preset Directives to {json.dumps(value, ensure_ascii = False)}")