from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ..._clients import ContextCore
from ....assist import PersonaInfo, SendMsg

withdraw = on_command("withdraw", aliases={"w", "Withdraw"}, rule=to_me(), block=True)

@withdraw.handle()
async def handle_withdraw(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Context.Withdraw", withdraw, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    context_core = ContextCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        if persona_info.args_str:
            try:
                num = int(persona_info.args_str)
            except ValueError:
                await send_msg.send_error("Please input a valid number")
            
            if num < 1:
                await send_msg.send_error("Please input a number greater than 0")
        else:
            num = 1

        response = await context_core.withdraw(num)

        if response.code == 200:
            await send_msg.send_prompt(
                f"Deleted: {response.data.deleted}\n"
                f"Remaining: {len(response.data.context)}\n"
            )
            
        else:
            await send_msg.send_response(response, "Withdraw Failed")
