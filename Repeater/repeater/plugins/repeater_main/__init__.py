# === Chat === #
from .commands.chat import *

# === Context === #
from .commands.context import *

# === Prompt === #
from .commands.prompt import *

# === Config === #
from .commands.config import *

# === Mixed === #
from .commands.mixed import *

# === Model Info === #
from .commands.model_info import *

# === More Interesting Tools === #
from .commands.more_interesting_tools import *

# === Var Expand === #
from .commands.variable_expansion import *

# === UserDataFile === #
from .commands.user_file import (
    handle_send_user_data_file,
)

# === SessionID === #
from .commands.get_namespace import handle_get_namespace

# === Readme === #
from .commands.send_readme_file import handle_send_readme_file

# === TextRender === #
from .commands.text_render import handle_text_render

# === Comment === #
from .commands.annotation import handle_annotation