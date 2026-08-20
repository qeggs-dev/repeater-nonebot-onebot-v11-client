from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class ModelRequestLoopTimes(BaseConfig):
    cmd = "modelRequestLoopTimes"
    aliases = {
        "mrlt",
        "MRLT",
        "model_request_loop_times",
        "Model_Request_Loop_Times",
        "ModelRequestLoopTimes",
        "MODEL_REQUEST_LOOP_TIMES",
    }
    field = "max_generate_times"
    description = f"""
    Number of times to regenerate.
    This number is consumed by model error retries and tool calls.

    Usage:
      /{cmd} <number>
    """

    async def parse_value(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
        raw_value: int,
    )  -> int:
        try:
            value = int(persona_info.message_stripped_str)
        except ValueError:
            await send_msg.send_error("Please input a number.")
        
        return max(1, value)
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: int
        ):
        await send_msg.send_response_check_code(response, f"Model Request Loop Times set to {value}")