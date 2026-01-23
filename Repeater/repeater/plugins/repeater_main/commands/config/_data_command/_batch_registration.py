from nonebot import on_command
from nonebot.rule import to_me, Rule
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from dataclasses import dataclass, field as dataclass_field
from typing import Callable, Type, Any

from ..._clients import ConfigCore
from ....assist import PersonaInfo, SendMsg

@dataclass
class CommandHandler:
    """
    命令处理器注册数据类
    """
    command: Callable[..., Type[Matcher]]
    component: str
    prompt: Callable[[PersonaInfo], str] | str | None = None
    names: list[str] = dataclass_field(default_factory=list)
    type_converter: Callable[[str], Any] | None = None
    config_key: str
    base_namespace: str = "Config"
    rule: Rule = to_me()
    block: bool = True

    @property
    def main_name(self) -> str:
        if self.names:
            return self.names[0]
        else:
            return self.__class__.__name__.lower()
    
    @property
    def other_names(self) -> set[str]:
        if len(self.names) > 1:
            return set(self.names[1:])
        else:
            return set()

class BatchRegistration:
    def __init__(self, component: str):
        self._component: str = component
        self._commands: dict[str, CommandHandler] = {}
    
    @staticmethod
    def register(command: CommandHandler):
        if not command.names:
            raise ValueError("names cannot be empty")
        component = f"{command.base_namespace}.{command.main_name}"
        matcher = on_command(command.main_name, aliases=command.other_names, rule = command.rule, block = command.block)
        
        @matcher.handle()
        async def handle(bot: Bot, event: MessageEvent, matcher: Matcher, args: Message = CommandArg()):
            persona_info = PersonaInfo(bot=bot, event=event, args=args)
            send_msg = SendMsg(component, matcher, persona_info)

            if send_msg.is_debug_mode:
                await send_msg.send_debug_mode()
            
            chat_core = ConfigCore(persona_info)
            if callable(command.type_converter):
                value = command.type_converter(persona_info)
            else:
                value = persona_info.message_str
            response = await chat_core.set_config(command.config_key, value)
            if callable(command.prompt):
                prompt = command.prompt(persona_info)
            else:
                prompt = command.prompt
            await send_msg.send_response_check_code(response, prompt)