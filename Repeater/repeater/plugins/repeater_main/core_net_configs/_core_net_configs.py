# 服务端配置
from ._net_config import net_config
from ._storage_configs import storage_configs

# ==== CHAT API ==== #
BACKEND_HOST = net_config.backend_host
BACKEND_PORT = net_config.backend_port
CHAT_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/chat/completion"
NPCHAT_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/chat/completion/noprompt"

# ==== CONTEXT API ==== #
DELETE_CONTEXT_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/context/delete"
GET_CONTEXT_LENGTH_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/context/length"
INJECT_CONTEXT_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/session/inject"
WIHTDRAW_CONTEXT_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/context/withdraw"
CHANGE_CONTEXT_BRANCH_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/context/change"
CLONE_CONTEXT_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/context/clone"

# ==== PROMPT API ==== #
SET_PROMPT_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/prompt/set"
DELETE_PROMPT_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/prompt/delete"
DELETE_SUBSESSION_PROMPT_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/prompt/subsession/delete"
CLONE_PROMPT_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/prompt/clone"

# ==== CONFIG API ==== #
SET_CONFIG_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/config/set"
GET_CONFIG_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/config/get"
REMOVE_CONFIG_KEY_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/config/delkey"
CHANGE_CONFIG_BRANCH_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/config/change"
DELETE_CONFIG_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/config/delete"
CLONE_CONFIG_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/config/clone"

# ==== MODEL API ==== #
GET_MODEL_UID_LIST = f"{BACKEND_HOST}:{BACKEND_PORT}/model/list"
GET_MODEL_INFO = f"{BACKEND_HOST}:{BACKEND_PORT}/model/info"
GET_MODEL_TYPES = f"{BACKEND_HOST}:{BACKEND_PORT}/model/types"

# ==== Download User Data File ==== #

DOWNLOAD_USER_DATA_FILE_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/userdata/file"

# ==== RENDER API ==== #
DOWNLOAD_RENDERED_IMAGE_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/file/render"
TEXT_RENDER_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/render"

# ==== ONLINE CHECK API ==== #
ONLINE_CHECK_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/server/online"

# ==== README API ==== #
README_FILE_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/readme.md"
HTML_README_FILE_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/readme.html"

# ==== Balance API ==== #
BALANCE_ROUTE = f"{BACKEND_HOST}:{BACKEND_PORT}/balance_query"

# ==== VARIABLE EXPANSION API ==== #
VARIABLE_EXPANSION = f"{BACKEND_HOST}:{BACKEND_PORT}/variable_expand"

# ==== CONFIG ==== #
HELLO_CONTENT = storage_configs.hello_content
RepeaterDebugMode = net_config.repeater_debug_mode # 是否开启调试模式，调试模式下，将直接返回消息内容，而不进行后端访问操作

