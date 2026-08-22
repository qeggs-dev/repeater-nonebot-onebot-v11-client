from abc import abstractmethod
from typing import Any, TypeVar, ClassVar, Generic

from ....clients import ConfigClient
from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....command_register import CommandPackage
from .operation_type import OperationType

T = TypeVar("T")

class BaseConfig(CommandPackage, Generic[T]):
    field: str = ""
    operation: ClassVar[OperationType] = OperationType.SET
    cmd_type = CmdTypes.CONFIG

    async def parse_value(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            raw_value: Any | None
        ) -> T:
        return persona_info.message_stripped_str
    
    async def parse_value_free(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            raw_value: Any | None
        ) -> tuple[str, T]:
        return self.field, await self.parse_value(persona_info, send_msg, raw_value)

    @abstractmethod
    async def finish_message(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
        response: Response[Any] | None,
        field: str | None,
        value: T | None
    ) -> None:
        pass

    async def get_client(
        self,
        persona_info: PersonaInfo,
    ):
        user_configs = await persona_info.get_user_configs()
        client = ConfigClient(persona_info, user_configs)
        return client
    
    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg) -> None:
        client = await self.get_client(persona_info)
        raw_value = None
        response: Response[Any] | None = None
        if self.operation in [OperationType.GET, OperationType.GET_AND_SET]:
            response = await client.get_configs()
            if not response:
                await send_msg.send_error_response(response)
            else:
                config: dict = response.json()
                raw_value = config.get(self.field)
        
        field, value = await self.parse_value_free(
            persona_info,
            send_msg,
            raw_value
        )
        match self.operation:
            case OperationType.SET:
                response = await client.set_config(field, value)
            case OperationType.GET_AND_SET:
                response = await client.set_config(field, value)
            case OperationType.GET:
                response = await client.get_configs()
            case OperationType.GET_FILE_URL:
                response = None
                value = client.get_configs_url()
        
        await self.finish_message(
            persona_info = persona_info,
            send_msg = send_msg,
            response = response,
            field = field,
            value = value
        )