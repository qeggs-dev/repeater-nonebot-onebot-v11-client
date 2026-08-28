from nonebot import logger
from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....command_register import(
    CommandCaller
)
from ....clients import (
    ContextClient,
    ChatClient,
    ContentRole,
    ChatResponse
)
from ..._bases import BaseChat, SendMessage

@CommandCaller.register
class Regenerate(BaseChat):
    cmd = "regenerate"
    aliases = {
        "reg",
        "REG",
        "Regenerate",
        "REGENERATE",
    }
    cmd_type = CmdTypes.MIXED
    empty_exit: bool = False
    description = f"""
    Recall the previous message and resend it.

    Usage:
    ```
    /{cmd}
    ```
    """
    
    async def send_message(
        self,
        client: ChatClient,
        send_messages: SendMessage,
        persona_info: PersonaInfo,
        send_msg: SendMsg
    ) -> Response[ChatResponse]:
        user_configs = await persona_info.get_user_configs()
        context_client = ContextClient(persona_info, user_configs)
        response = await context_client.withdraw()
        
        if response:
            data = response.get_data()
            if data is None:
                await send_msg.send_error(
                    "Unable to process data."
                )
                send_msg.break_handler()
            await send_msg.send_prompt(
                (
                    f"Deleted: {data.deleted}\n"
                    f"Remaining: {len(data.context)}\n"
                ),
                continue_handler = True
            )
        else:
            await send_msg.send_response_check_code(response, "Withdraw Failed")
            send_msg.break_handler()
        
        context = data.deleted_context
        user_input: list[str] = []
        for unit in context:
            if unit.role == ContentRole.USER:
                user_input.append(
                    self.sub_user_raw_input(unit.content)
                )

        send_messages.text = "\n\n".join(user_input)

        return await super().send_message(
            client,
            send_messages,
            persona_info,
            send_msg
        )
    
    @staticmethod
    def sub_user_raw_input(user_input: str) -> str:
        return ChatClient.metadata_pattern.sub("", user_input)