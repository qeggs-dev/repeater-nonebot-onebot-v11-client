from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot
from nonebot import logger

from .._clients import PromptCore, ChatCore
from ...assist import PersonaInfo, SendMsg
from ...storage import async_text_storage
from ._default_meta_prompt import META_PROMPT

generate_prompt = on_command("generatePrompt", aliases={"gp", "generate_prompt", "Generate_Prompt", "GeneratePrompt"}, rule=to_me(), block=True)

@generate_prompt.handle()
async def handle_generate_prompt(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    sendmsg = SendMsg("Prompt.Generater", generate_prompt, persona_info)

    msg = persona_info.message_str.strip()

    meta_prompt_file_path = "prompts/generate_prompt/meta_prompt.txt"
    try:
        meta_prompt = await async_text_storage.load(
            path = meta_prompt_file_path,
        )
    except Exception as e:
        logger.error(f"load meta_prompt.txt failed: {e}")
        meta_prompt = META_PROMPT
        await async_text_storage.save(
            path = meta_prompt_file_path,
            data = meta_prompt
        )

    if sendmsg.is_debug_mode:
        await sendmsg.send_debug_mode()
    else:
        chat_core = ChatCore(persona_info, namespace="Prompt_Generater")
        prompt = [
            msg
        ]
        chat_response = await chat_core.send_message(
            "\n".join(prompt),
            add_metadata = False,
            save_context = False,
            temporary_prompt = meta_prompt
        )
        
        if chat_response.code != 200:
            await sendmsg.send_response(
                chat_response, "Generate Prompt failed."
            )
        if chat_response.data is None:
            await sendmsg.send_error(
                "No prompt generated."
            )
        if not chat_response.data.content:
            await sendmsg.send_error(
                "No prompt content generated."
            )
        
        prompt_core = PromptCore(persona_info)
        prompt_response = await prompt_core.set_prompt(
            chat_response.data.content
        )
        if prompt_response.code != 200:
            await sendmsg.send_response(
                prompt_response,
                "Set Prompt failed"
            )
        else:
            await sendmsg.send_mixed_render(
                text = "Prompt generated:",
                text_to_render = chat_response.data.content,
                prompt_mode = True
            )
