from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ..._clients import PromptCore
from ....assist import PersonaInfo, SendMsg

setprompt = on_command("setPrompt", aliases={"sp", "set_prompt", "Set_Prompt", "SetPrompt"}, rule=to_me(), block=True)


@setprompt.handle()
async def handle_setprompt(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Prompt.Set_Prompt", setprompt, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    msg = persona_info.message_str.strip()
    
    prompt_core = PromptCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await prompt_core.set_prompt(msg)
        await send_msg.send_response(response, f"Set Prompt {'successfully' if response.code == 200 else 'failed'}")
