import platform
import os
import sys
import json
import time
import shlex
from pathlib import Path
import ctypes
import subprocess
import threading
from dataclasses import dataclass

PROJECT_PATH = "./Repeater"
SYSTEM = platform.system()
TITLE = "Repeater"
CONSOLE_TITLE = f"{TITLE} Nonebot Plugin"

def init_config(path: str | os.PathLike = "./run.json"):
    global PROJECT_PATH, SYSTEM, TITLE, CONSOLE_TITLE
    config_file_path = Path(path)
    if config_file_path.exists():
        with open(config_file_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        PROJECT_PATH = config.get("project_path", PROJECT_PATH)
        SYSTEM = config.get("system", SYSTEM)
        TITLE = config.get("title", TITLE)
        CONSOLE_TITLE = config.get("console_title", CONSOLE_TITLE)
    else:
        with open(config_file_path, "w", encoding="utf-8") as f:
            json.dump({
                "project_path": PROJECT_PATH,
                "system": SYSTEM,
                "title": TITLE,
                "console_title": CONSOLE_TITLE
            }, f, ensure_ascii=False, indent=4)

def set_title(text: str) -> None:
    if SYSTEM == "Windows":
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleTitleW(text)
    else:
        sys.stdout.write(f"\x1b]2;{text}\x07")
        sys.stdout.flush()

@dataclass
class Process_Command:
    cmd: list[str]
    print_runtime: bool = True
    print_return: bool = True

def create_cmd():
    if SYSTEM == "Windows":
        cmd: list[Process_Command] = [
            Process_Command(
                [".venv/Scripts/python.exe", "-c" "import sys; print(f\"Run script with Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} for Windows\")"],
                print_runtime=False,
                print_return=False
            ),
            Process_Command(
                [".venv/Scripts/nb", "run"]
            )
        ]
    else:
        cmd: list[Process_Command] = [
            Process_Command(
                [".venv/bin/python3", "-c", "import sys; print(f\"Run script with Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} for " + SYSTEM + "\")"],
                print_runtime=False,
                print_return=False
            ),
            Process_Command(
                [".venv/bin/nb", "run"]
            )
        ]
    return cmd

def format_time_duration(duration: int, start_with: int = 0, use_abbreviation: bool = False, delimiter: str = ", ") -> str:
    """
    Format time duration in nanoseconds to a human-readable string.

    Args:
        duration (int): Time duration in nanoseconds.
        start_with (int, optional): The minimum level required for the selection when you want to format, 
                                  the range is [0,9). Defaults to 0.
        use_abbreviation (bool, optional): Whether to use abbreviations for time units. Defaults to False.

    Returns:
        str: Formatted time duration string.
    """
    if start_with not in range(0, 10):
        raise ValueError("start_with must be in range [0, 9)")
    
    # Handle zero duration
    if duration == 0:
        return "0 ns" if use_abbreviation else "0 nanoseconds"
    
    # Handle negative duration
    is_negative = duration < 0
    duration = abs(duration)
    
    levels: list[tuple[str, str, int]] = [
        ("nanosecond", "ns", 1000),
        ("microsecond", "μs", 1000),
        ("millisecond", "ms", 1000),
        ("second", "s", 60),
        ("minute", "min", 60),
        ("hour", "h", 24),
        ("day", "day", 30),
        ("month", "mon", 12),
        ("year", "y", 100),
    ]
    end_level: str = "century"
    end_level_abbreviation: str = "cent"
    
    data_level_stack: list[str] = []
    remaining_part: int = duration
    
    # Process each level starting from the specified level
    for name, abbreviation, divisor in levels[start_with:]:
        if remaining_part == 0:
            break
            
        current_value = remaining_part % divisor
        remaining_part //= divisor
        
        if current_value > 0:
            unit = abbreviation if use_abbreviation else name
            # Handle pluralization
            if current_value != 1 and not use_abbreviation:
                unit += "s"
            data_level_stack.append(f"{current_value} {unit}")
        
        if remaining_part == 0:
            break
    
    # Handle the final level (century)
    if remaining_part > 0:
        unit = end_level_abbreviation if use_abbreviation else end_level
        if remaining_part != 1 and not use_abbreviation:
            unit += "s"
        data_level_stack.append(f"{remaining_part} {unit}")
    
    # Reverse the stack to get the correct order (largest to smallest)
    text = delimiter.join(data_level_stack[::-1])
    
    if is_negative:
        text = f"(Negative) {text}"
    
    return text

class Process:
    def __init__(self, *cmds:str) -> None:
        self._cmd = list(cmds)
        self._start: int = 0
        self._end: int = 0
        self._process: subprocess.CompletedProcess[bytes] | None = None
    
    def run_with(self, cwd: str | Path):
        self._start = time.monotonic_ns()
        try:
            result: subprocess.CompletedProcess[bytes] = subprocess.run(
                self._cmd,
                cwd = cwd
            )
        finally:
            self._end = time.monotonic_ns()
        result.returncode
        self._process = result
        return result

    def run(self):
        return self.run_with(Path.cwd())
    
    @property
    def returncode(self) -> int:
        if self._process is not None:
            return self._process.returncode
        return -1
    
    @property
    def cmd(self) -> str:
        return shlex.join(self._cmd)
    
    @property
    def start(self) -> int:
        return self._start

    @property
    def end(self) -> int:
        return self._end

def run_process(*cmds: Process_Command):
    for cmd in cmds:
        process = Process(*cmd.cmd)
        process.run_with(PROJECT_PATH)
        if cmd.print_runtime or cmd.print_return:
            print(f"Process:\n{process.cmd}")
        if cmd.print_runtime:
            print(f"  - took {format_time_duration(process.end - process.start)}")
        if cmd.print_return:
            print(f"  - return code: {process.returncode}")
    
    return process

def pause():
    try:
        empty_event = threading.Event()
        empty_event.wait()
    except Exception:
        pass

def main():
    set_title(TITLE)
    print(CONSOLE_TITLE.center(os.get_terminal_size().columns))
    print("=" * os.get_terminal_size().columns)
    print(f"Run With Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    cmd = create_cmd()
    while True:
        try:
            run_process(*cmd)
        except KeyboardInterrupt:
            print("User interrupted")
        
        try:
            input_str = input("Run Again? [Y/n] ")
        except KeyboardInterrupt:
            print("User interrupted")
            continue

        if input_str.lower() not in ["n", "no", "false", "0"]:
            continue
        else:
            break

if __name__ == "__main__":
    try:
        init_config()
        main()
    except Exception as e:
        import traceback
        with open("traceback.txt", "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        raise