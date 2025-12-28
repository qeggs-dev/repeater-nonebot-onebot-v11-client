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
    sendmsg = SendMsg("Model.Get_Model_List", get_model_list, persona_info)

    try:
        auto_save_context = str_to_bool(persona_info.message_str)
    except ValueError:
        await sendmsg.send_error("Not a valid boolean value")

    if sendmsg.is_debug_mode:
        await sendmsg.send_debug_mode()
    else:
        model_info_core = ModelInfoCore()
        model_type_str = persona_info.message_str.strip()
        if model_type_str in MODEL_TYPES:
            model_type = ModelType(model_type_str)
        else:
            await sendmsg.send_error("Not a valid model type")

        response = await model_info_core.get_model_list(model_type)
        if response.code == 200:
            if response.data is not None:
                await sendmsg.send_check_length("\n".join(response.data))
            else:
                await sendmsg.send_error("Error: No Model Data")
        else:
            await sendmsg.send_response(response)

