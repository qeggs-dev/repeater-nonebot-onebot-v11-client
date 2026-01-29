# 服务端配置
from ._net_config import net_config
from ._storage_configs import storage_configs

# ==== BASE URL ==== #
BACKEND_HOST = net_config.backend_host
BACKEND_PORT = net_config.backend_port
BASE_URL = f"{BACKEND_HOST}:{BACKEND_PORT}"

# ==== CHAT API ==== #
CHAT_ROUTE = f"{BASE_URL}/chat/completion"
NPCHAT_ROUTE = f"{BASE_URL}/chat/completion/noprompt"

# ==== CONTEXT API ==== #
DELETE_CONTEXT_ROUTE = f"{BASE_URL}/userdata/context/delete"
GET_CONTEXT_LENGTH_ROUTE = f"{BASE_URL}/userdata/context/length"
ROLE_STRUCTRUE_ROUTE = f"{BASE_URL}/userdata/context/structure_check/role"
INJECT_CONTEXT_ROUTE = f"{BASE_URL}/session/inject"
WIHTDRAW_CONTEXT_ROUTE = f"{BASE_URL}/userdata/context/withdraw"
CHANGE_CONTEXT_BRANCH_ROUTE = f"{BASE_URL}/userdata/context/change"

# ==== PROMPT API ==== #
SET_PROMPT_ROUTE = f"{BASE_URL}/userdata/prompt/set"
DELETE_PROMPT_ROUTE = f"{BASE_URL}/userdata/prompt/delete"
DELETE_SUBSESSION_PROMPT_ROUTE = f"{BASE_URL}/prompt/subsession/delete"
CLONE_PROMPT_ROUTE = f"{BASE_URL}/prompt/clone"

# ==== CONFIG API ==== #
SET_CONFIG_ROUTE = f"{BASE_URL}/userdata/config/set"
GET_CONFIG_ROUTE = f"{BASE_URL}/userdata/config/get"
REMOVE_CONFIG_KEY_ROUTE = f"{BASE_URL}/userdata/config/delkey"
CHANGE_CONFIG_BRANCH_ROUTE = f"{BASE_URL}/userdata/config/change"
DELETE_CONFIG_ROUTE = f"{BASE_URL}/userdata/config/delete"
CLONE_CONFIG_ROUTE = f"{BASE_URL}/config/clone"

# ==== MODEL API ==== #
GET_MODEL_UID_LIST = f"{BASE_URL}/model/list"
GET_MODEL_INFO = f"{BASE_URL}/model/info"
GET_MODEL_TYPES = f"{BASE_URL}/model/types"

# ==== Download User Data File ==== #

DOWNLOAD_USER_DATA_FILE_ROUTE = f"{BASE_URL}/userdata/file"

# ==== RENDER API ==== #
DOWNLOAD_RENDERED_IMAGE_ROUTE = f"{BASE_URL}/file/render"
TEXT_RENDER_ROUTE = f"{BASE_URL}/render"

# ==== ONLINE CHECK API ==== #
ONLINE_CHECK_ROUTE = f"{BASE_URL}/server/online"

# ==== README API ==== #
README_FILE_ROUTE = f"{BASE_URL}/readme.md"
HTML_README_FILE_ROUTE = f"{BASE_URL}/readme.html"

# ==== Balance API ==== #
BALANCE_ROUTE = f"{BASE_URL}/balance_query"

# ==== VARIABLE EXPANSION API ==== #
VARIABLE_EXPANSION = f"{BASE_URL}/variable_expand"

# ==== VERSION API ==== #
VERSION_ROUTE = f"{BASE_URL}/version"

# ==== CONFIG ==== #
HELLO_CONTENT = storage_configs.hello_content
RepeaterDebugMode = net_config.repeater_debug_mode # 是否开启调试模式，调试模式下，将直接返回消息内容，而不进行后端访问操作

