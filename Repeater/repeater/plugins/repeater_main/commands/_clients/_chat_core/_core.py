import json
from typing import (
    Any,
    Literal,
    AsyncIterator
)
import httpx
from ._response_body import ChatResponse, StreamChatChunkResponse
from ....exit_register import ExitRegister
from ....assist import PersonaInfo, Response

from ....core_net_configs import *

exit_register = ExitRegister()

class ChatCore:
    _chat_client = httpx.AsyncClient(timeout=storage_configs.server_api_timeout.chat)
    _client = httpx.AsyncClient()
    
    def __init__(self, persona_info: PersonaInfo, public_space_chat: bool = False, namespace: str | None = None):
        self._persona_info = persona_info
        self._namespace = namespace
        self._public_space_chat: bool = public_space_chat
    
    @property
    def namespace(self) -> str:
        if self._namespace:
            return self._namespace
        elif self._public_space_chat:
            return self._persona_info.namespace.public_space_id
        else:
            return self._persona_info.namespace_str
    
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
        enable_md_prompt: bool = True,
        reference_context_id: str | None = None,
        continue_completion: bool | None = None,
    ) -> Response[ChatResponse | None]:
        """
        发送消息到AI后端
        
        :param message: 消息内容
        :param username: 用户名
        :
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
            reference_context_id = reference_context_id,
            continue_completion = continue_completion,
        )
        response = await self._chat_client.post(
            url = url,
            json = data
        )
        if response.status_code == 200:
            try:
                result:dict = response.json()
            except json.JSONDecodeError:
                return Response(
                    code = response.status_code,
                    text = response.text,
                    data = None
                )
        try:
            response_body = ChatResponse(
                **result
            )
        except Exception as e:
            response_body = None
            
        return Response(
            code = response.status_code,
            text = response.text,
            data = response_body
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
        enable_md_prompt: bool = True,
        reference_context_id: str | None = None,
        continue_completion: bool | None = None,
    ) -> AsyncIterator[Any]:
        """
        发送消息到AI后端，并获取流式响应
        
        :param message: 消息内容
        :param username: 用户名
        :
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
            reference_context_id = reference_context_id,
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
        enable_md_prompt: bool = True,
        reference_context_id: str | None = None,
        continue_completion: bool | None = None,
        stream: bool = False,
    ):
        # 表单数据格式 (Form Data)
        data = {
            "user_info": {
                "username" : self._persona_info.nickname,
                "nickname" : self._persona_info.display_name,
                "age": self._persona_info.age,
                "gender": self._persona_info.gender,
            },
        }
        if load_prompt is not None:
            data["load_prompt"] = load_prompt
        if save_context is not None:
            data["save_context"] = save_context
        if model_uid is not None:
            data["model_uid"] = model_uid
        if image_url:
            data["image_url"] = image_url
        if role_name is not None:
            data["role_name"] = role_name
        elif storage_configs.merge_group_id:
            data["role_name"] = self._persona_info.nickname
        if reference_context_id:
            data["reference_context_id"] = reference_context_id
        if continue_completion is not None:
            data["continue_completion"] = continue_completion
        if temporary_prompt is not None:
            data["temporary_prompt"] = temporary_prompt
        if stream:
            data["stream"] = stream
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
                if reference_context_id:
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