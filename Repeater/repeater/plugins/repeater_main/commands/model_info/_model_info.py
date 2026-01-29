from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from .._clients import ModelInfoCore, MODEL_TYPES, ModelType
from ...assist import PersonaInfo, SendMsg, str_to_bool

get_model_list = on_command("getModelList", aliases={"gml", "get_model_list", "Get_Model_List", "GetModelList"}, rule=to_me(), block=True)

@get_model_list.handle()
async def handle_get_model_list(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Model.Get_Model_List", get_model_list, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        model_info_core = ModelInfoCore()
        model_type_str = persona_info.message_str.strip()
        if model_type_str in MODEL_TYPES:
            model_type = ModelType(model_type_str)
        else:
            await send_msg.send_error("Not a valid model type")

        response = await model_info_core.get_model_list(model_type)
        if response.code == 200:
            model_list = response.get_data()
            if model_list is None:
                await send_msg.send_error("Error: No Model Data")
            elif not isinstance(model_list, list):
                await send_msg.send_error("Response data is not a list")
            else:
                text_buffer: list[str] = []
                for model in model_list:
                    text_buffer.append(f"{model.uid} ({model.parent}/{model.name})")
                await send_msg.send_check_length("\n".join(text_buffer))
        else:
            await send_msg.send_response_check_code(response)

