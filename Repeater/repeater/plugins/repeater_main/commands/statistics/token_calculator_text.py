from ...assist import SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller
)
from .token_calculator import TokenCalculator

@CommandCaller.register
class TokenCalculatorText(TokenCalculator):
    cmd = "tokenizer_text"
    aliases = {
        "tizt",
        "TIZT",
        "Tokenizer_Text",
        "TOKENIZER_TEXT"
    }
    cmd_type = CmdTypes.STATISTIC

    async def output(
            self,
            send_msg: SendMsg,
            tokens_count: int,
            text_count: int,
            most_frequent: list[str]
        ):
        most_frequent_text = "\n  - ".join(most_frequent)
        await send_msg.send_mixed_render(
            "\n".join(
                [
                    f"Token count: {tokens_count}",
                    f"Text length: {text_count}",
                    f"Average something conversion rate: {tokens_count / text_count:.2%}(1:{tokens_count / text_count:.2f})",
                    most_frequent_text
                ]
            ),
        )