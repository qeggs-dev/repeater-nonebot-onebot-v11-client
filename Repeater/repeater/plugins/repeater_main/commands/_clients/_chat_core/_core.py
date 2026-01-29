import json
from typing import (
    Any,
    Literal,
    AsyncIterator
)
import httpx
from ._response_body import ChatResponse, StreamChatChunkResponse
from ._cross_user_data_routing import CrossUserDataRouting, DataRoutingField
from ....exit_register import ExitRegister
from ....assist import PersonaInfo, Response
from ....core_net_configs import *

exit_register = ExitRegister()

class ChatCore:
    _chat_client = httpx.AsyncClient(timeout=storage_configs.server_api_timeout.chat)
    _client = httpx.AsyncClient()
    
    def __init__(self, persona_info: PersonaInfo, namespace: str | None = None):
        self._persona_info = persona_info
        self._namespace = namespace
    
    @property
    def namespace(self) -> str:
        if self._namespace:
            return self._namespace
        else:
            return self._persona_info.namespace_str
    
    @property
    def merge_group_id(self) -> str | None:
        if storage_configs.merge_group_id:
            return self._persona_info.namespace.merge_group_id
        return None
    
    async def send_message(
        self,
        message: str | None = None,
        add_metadata: bool = True,
        role_name: str | None = None,
        temporary_prompt: str | None = None,
        model_uid: str | None = None,
        image_url: str | list[str] | None = None,
        load_prompt: bool | None = None,
        save_context: bool | None = None,
        save_new_only: bool | None = None,
        enable_md_prompt: bool = True,
        cross_user_data_routing: str | None = None,
        continue_completion: bool | None = None,
    ) -> Response[ChatResponse]:
        """
        发送消息到AI后端
        
        :param message: 消息内容
        :param add_metadata: 是否添加元数据
        :param role_name: 角色名称
        :param temporary_prompt: 临时提示
        :param model_uid: 模型UID
        :param image_url: 图片URL
        :param load_prompt: 是否加载提示
        :param save_context: 是否保存上下文
        :param save_new_only: 是否只保存新内容
        :param enable_md_prompt: 是否启用Markdown提示
        :param cross_user_data_routing: 跨用户数据路由
        :param continue_completion: 是否继续生成
        :return: AI返回的消息
        """
        url = f"{CHAT_ROUTE}/{self.namespace}"
        data = self._prepare_request_body(
            message = message,
            add_metadata = add_metadata,
            role_name = role_name,
            temporary_prompt = temporary_prompt,
            model_uid = model_uid,
            image_url = image_url,
            load_prompt = load_prompt,
            enable_md_prompt = enable_md_prompt,
            save_context = save_context,
            save_new_only = save_new_only,
            cross_user_data_routing = cross_user_data_routing,
            continue_completion = continue_completion,
        )
        response = await self._chat_client.post(
            url = url,
            json = data
        )
            
        return Response(
            response,
            ChatResponse
        )
    
    async def send_stream_message(
        self,
        message: str,
        add_metadata: bool = True,
        role_name: str | None = None,
        temporary_prompt: str | None = None,
        model_uid: str | None = None,
        image_url: str | list[str] | None = None,
        load_prompt: bool | None = None,
        save_context: bool | None = None,
        save_new_only: bool | None = None,
        enable_md_prompt: bool = True,
        cross_user_data_routing: str | None = None,
        continue_completion: bool | None = None,
    ) -> AsyncIterator[Any]:
        """
        发送消息到AI后端，并获取流式响应
        
        :param message: 消息内容
        :param add_metadata: 是否添加元数据
        :param role_name: 角色名称
        :param temporary_prompt: 临时提示
        :param model_uid: 模型UID
        :param image_url: 图片URL
        :param load_prompt: 是否加载提示
        :param save_context: 是否保存上下文
        :param save_new_only: 是否只保存新内容
        :param enable_md_prompt: 是否启用Markdown提示
        :param cross_user_data_routing: 跨用户数据路由
        :param continue_completion: 是否继续生成
        :return: AI返回的消息
        """
        import json
        url = f"{CHAT_ROUTE}/{self.namespace}"
        data = self._prepare_request_body(
            message = message,
            add_metadata = add_metadata,
            role_name = role_name,
            temporary_prompt = temporary_prompt,
            model_uid = model_uid,
            image_url = image_url,
            load_prompt = load_prompt,
            enable_md_prompt = enable_md_prompt,
            save_context = save_context,
            save_new_only = save_new_only,
            cross_user_data_routing = cross_user_data_routing,
            continue_completion = continue_completion,
            stream = True,
        )
        async with self._chat_client.stream(
            method="POST",
            url=url,
            json=data  # 使用 json= 表示请求体数据
        ) as response:
            response.raise_for_status()
            
            async for line in response.aiter_lines():
                if not line.strip():
                    continue

                yield StreamChatChunkResponse(**json.loads(line))
    
    @staticmethod
    def _merge_dict(base: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        base_copy = base.copy()
        for key, value in kwargs.items():
            if value is not None:
                base_copy[key] = value
        return base_copy
    
    def _prepare_request_body(
        self,
        message: str | None = None,
        add_metadata: bool = True,
        role_name: str | None = None,
        temporary_prompt: str | None = None,
        model_uid: str | None = None,
        image_url: str | list[str] | None = None,
        load_prompt: bool | None = None,
        save_context: bool | None = None,
        save_new_only: bool | None = None,
        enable_md_prompt: bool = True,
        cross_user_data_routing: CrossUserDataRouting | None = None,
        continue_completion: bool | None = None,
        stream: bool | None = None,
    ):
        # 表单数据格式 (Form Data)
        base_data = {
            "user_info": {
                "username" : self._persona_info.nickname,
                "nickname" : self._persona_info.display_name,
                "age": self._persona_info.age,
                "gender": self._persona_info.gender,
            },
        }
        data = self._merge_dict(
            base = base_data,
            load_prompt = load_prompt,
            save_context = save_context,
            save_new_only = save_new_only,
            model_uid = model_uid,
            continue_completion = continue_completion,
            temporary_prompt = temporary_prompt,
            stream = stream,
        )
        if image_url:
            data["image_url"] = image_url
        
        if role_name is not None:
            data["role_name"] = role_name
        elif storage_configs.merge_group_id:
            data["role_name"] = self._persona_info.nickname
        
        if cross_user_data_routing is not None:
            data["cross_user_data_routing"] = cross_user_data_routing.model_dump(exclude_none=True)
        elif self.merge_group_id:
            cross_user_data_routing = CrossUserDataRouting()
            cross_user_data_routing.context.fill_missing(self.merge_group_id)
            data["cross_user_data_routing"] = cross_user_data_routing.model_dump(exclude_none=True)

        if message:
            message_buffer:list[str] = []
            if add_metadata:
                message_buffer.append("> MessageMetadata:")
                message_buffer.append(f">     Message Type: {self._persona_info.source.value}")
                message_buffer.append(">     Message Sending time:{time}")
                if enable_md_prompt:
                    message_buffer.append(">     Markdown Rendering is turned on!!")
                if storage_configs.merge_group_id:
                    message_buffer.append(">     Now User: {username}({nickname})")
                if cross_user_data_routing:
                    message_buffer.append(">     Guest Mode(User: {username}), Citation context is turned on!!")
                message_buffer.append("\n---\n")
            message_buffer.append(message)
            data["message"] = "\n".join(message_buffer)
        return data
    
    exit_register.register()
    async def close(self):
        await self._chat_client.aclose()
        await self._client.aclose()
    # endregion