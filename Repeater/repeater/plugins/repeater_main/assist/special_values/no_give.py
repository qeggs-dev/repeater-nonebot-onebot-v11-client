from typing import Self, Any, TypeGuard

class NoGive:
    """
    Use to distinguish default values for parameters that are not given.
    """
    _instance: Self | None = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def is_no_give(cls, value: Any) -> TypeGuard[Self]:
        return value is cls._instance

    @classmethod
    def is_no_give_type(cls, value: type) -> TypeGuard[type[Self]]:
        return type(value) is type and issubclass(value, cls)