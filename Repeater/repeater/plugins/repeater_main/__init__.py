import time as _time
from .logger import logger as _logger

_logger.info(
    "Repeater onebot plugin loading..."
)

start_import_time = _time.perf_counter_ns()

try:
    from ._import_plugins import *
finally:
    end_import_time = _time.perf_counter_ns()
    _logger.info(
        "Import time: {import_time:.2f}s",
        import_time = (end_import_time - start_import_time) / 1e9
    )

_logger.info(
    "Repeater onebot plugin loaded."
)