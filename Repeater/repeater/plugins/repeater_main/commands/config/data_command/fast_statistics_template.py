from ....assist import PersonaInfo, SendMsg, Response
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class FastStatisticsTemplate(BaseConfig):
    cmd = "fastStatisticsTemplate"
    aliases = {
        "fst",
        "FST",
        "fast_statistics_template",
        "Fast_Statistics_Template",
        "FastStatisticsTemplate",
        "FAST_STATISTICS_TEMPLATE"
    }
    field = "request_statistics_template"
    description = f"""
    Set Fast Statistics Template

    Usage:
      /{cmd} template_text
    """
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: str
        ):
        await send_msg.send_response_check_code(response, f"Fast Statistics Template set to {value}")