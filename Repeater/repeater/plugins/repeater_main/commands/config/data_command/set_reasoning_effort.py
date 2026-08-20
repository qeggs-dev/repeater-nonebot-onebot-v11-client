from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig
from enum import StrEnum

@CommandCaller.register
class SetReasoningEffort(BaseConfig):
    cmd = "setReasoningEffort"
    aliases = {
        "sre",
        "SRE",
        "set_reasoning_effort",
        "Set_Reasoning_Effort",
        "SetReasoningEffort",
        "Set_Reasoning_Effort",
    }
    field = "reasoning_effort"
    description = f"""
    Set Reasoning Effort

    Usage:
      /{cmd} low
      /{cmd} medium
      /{cmd} high
      /{cmd} xhigh
      /{cmd} max
    """

    class ReasoningEffort(StrEnum):
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"
        XHIGH = "xhigh"
        MAX = "max"

    async def parse_value(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
        raw_value: str | None,
    )  -> str | None:
        msg = persona_info.message_stripped_str
        if msg.lower() in ["null", "none"]:
            return None
        try:
            value = self.ReasoningEffort(msg)
        except ValueError:
            await send_msg.send_error(
                "Invalid value, please use one of the following: "
                + ", ".join(self.ReasoningEffort.__members__.keys())
            )

        return value.value
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: str | None
        ):
        await send_msg.send_response_check_code(response, f"Set Reasoning Effort to {value}")