from enum import StrEnum

class ModelType(StrEnum):
    """Model types"""
    CHAT = "chat"

MODEL_TYPES = set(model_type.value for model_type in ModelType)