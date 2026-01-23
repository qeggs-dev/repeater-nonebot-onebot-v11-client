from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot
from nonebot import logger

from ..._clients import PromptCore, ChatCore
from ....assist import PersonaInfo, SendMsg
from ....storage import async_text_storage
from ._default_meta_prompt import META_PROMPT

generate_prompt = on_command("generatePrompt", aliases={"gp", "generate_prompt", "Generate_Prompt", "GeneratePrompt"}, rule=to_me(), block=True)

@generate_prompt.handle()
async def handle_generate_prompt(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Mixed.Prompt_Generater", generate_prompt, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    message = persona_info.message_str.strip()

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
    
    chat_core = ChatCore(persona_info, namespace="Prompt_Generater")
    image_url = await persona_info.get_images_url()
    chat_response = await chat_core.send_message(
        message,
        add_metadata = False,
        save_context = False,
        image_url = image_url,
        temporary_prompt = meta_prompt
    )
    
    if chat_response.code != 200:
        await send_msg.send_response_check_code(
            chat_response, "Generate Prompt failed."
        )
    data = chat_response.get_data()
    if data is None:
        await send_msg.send_error(
            "Unable to process data."
        )
    if data is None:
        await send_msg.send_error(
            "No prompt generated."
        )
    if not data.content:
        await send_msg.send_error(
            "No prompt content generated."
        )
    
    prompt_core = PromptCore(persona_info)
    prompt_response = await prompt_core.set_prompt(
        data.content
    )
    if prompt_response.code != 200:
        await send_msg.send_response_check_code(
            prompt_response,
            "Set Prompt failed"
        )
    else:
        await send_msg.send_mixed_render(
            text = "Prompt generated:",
            text_to_render = data.content,
            prompt_mode = True
        )
