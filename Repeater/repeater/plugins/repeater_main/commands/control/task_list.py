import time
from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)

@CommandCaller.register
class TaskList(CommandPackage):
    cmd = "taskList"
    aliases = {
        "tl",
        "TL",
        "task_list",
        "TaskList",
        "Tast_List",
        "TASK_LIST",
    }
    cmd_type = CmdTypes.CONTROL
    description = f"""
    Show all tasks.

    Usage: 
    ```
    /{cmd}
    ```
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        task_list = CommandCaller.get_user_runnings(persona_info.namespace)
        now_monotonic_time = time.perf_counter_ns()
        if task_list:
            text_buffer: list[str] = []
            for task in task_list:
                text_buffer.append(f"[{task.task_id}]")
                text_buffer.append(f"- {task.package.component}(Running for {(now_monotonic_time - task.start_monotonic_time) / 1e6:.3f}ms)")
            await send_msg.send_check_length_prompt("\n".join(text_buffer))
        else:
            await send_msg.send_error("No running tasks.")