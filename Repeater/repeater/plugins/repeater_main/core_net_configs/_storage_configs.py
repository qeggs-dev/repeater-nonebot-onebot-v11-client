from pydantic import BaseModel, Field
from typing import Generic, TypeVar
from ..config_loader import Loader, Mode

T = TypeVar("T")

class TextLengthScoreThreshold(BaseModel):
    group: float = 1.0
    private: float = 2.48

class TextLengthScoreConfigs(BaseModel):
    max_lines: int = 5
    single_line_max: int = 64
    mean_line_max: int = 32
    total_length: int = 400
    threshold: TextLengthScoreThreshold = Field(default_factory = TextLengthScoreThreshold)

class ServerAPITimeout(BaseModel):
    chat: float = 600.0
    context: float = 10.0
    prompt: float = 10.0
    config: float = 10.0
    variable_expansion: float = 40.0
    render: float = 600.0

class StorageConfigs(BaseModel):
    text_length_score_configs: TextLengthScoreConfigs = Field(default_factory = TextLengthScoreConfigs)
    reason_model_uid: str = "reasoner"
    hello_content: str = "Repeater Is Ready!"
    welcome_messages_by_weekday: dict[int | str, str] = Field(default_factory=dict, max_length=7)
    merge_group_id: bool = False
    server_api_timeout:ServerAPITimeout = Field(default_factory = ServerAPITimeout)
    use_base64_visual_input: bool = True
    download_visual_input_timeout: float = 600.0
    summarize_and_contract_default_message: str = "System Message: please sum up all the contents above."

loader: Loader[StorageConfigs] = Loader(
    model=StorageConfigs,
    path="configs/main_api.json",
    mode=Mode.JSON
)
storage_configs: StorageConfigs = loader.load(write_on_failure=True)