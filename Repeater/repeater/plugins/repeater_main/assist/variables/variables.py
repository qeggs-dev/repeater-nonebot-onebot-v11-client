from typing import TypeVar, Generic
from ..user_config import UserConfigs

T = TypeVar("T")
T_Default = TypeVar("T_Default")

class Variables(Generic[T], dict[str, T]):
    """
    Variables Manager
    """
    def load(self, configs: UserConfigs, name: str | None = None):
        if name is None:
            if configs.variables is not None:
                self.clear()
                self.update(configs.variables)
        else:
            if configs.variables is not None and name in configs.variables:
                self[name] = configs.variables[name]

    def dump(self, configs: UserConfigs, name: str | None = None):
        if name is None:
            configs.variables = self.copy()
        else:
            if configs.variables is None:
                configs.variables = {}
            configs.variables[name] = self[name]