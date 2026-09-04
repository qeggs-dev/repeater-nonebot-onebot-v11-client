import uuid
from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)

@CommandCaller.register
class CancelAll(CommandPackage):
    cmd = "cancelAll"
    aliases = {
        "cla",
        "CLA",
        "cancel_all",
        "Cancel_All",
        "CancelAll",
        "CANCEL_ALL",
    }
    cmd_type = CmdTypes.CONTROL
    description = f"""
    Cancel all tasks where component or trigger match.

    Usage: 
    ```
    /{cmd} component
    ```
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        trigger_or_component = persona_info.message_stripped_str
        try:
            package = CommandCaller.match_trigger_or_component(trigger_or_component)
        except KeyError:
            await send_msg("Command not found.")
            return

        instance = CommandCaller.get_instance(package)
        component: str = instance.component

        async with CommandCaller.running_lock:
            task_ids = CommandCaller.running_map.get(persona_info.namespace, set()).copy()
            cancelled: set[uuid.UUID] = set()
            for task_id in task_ids:
                try:
                    task = CommandCaller.runnings[task_id]
                except KeyError:
                    continue
                if type(task.package) is package:
                    task.cancel()
                    cancelled.add(task_id)
        
        if cancelled:
            text_buffer: list[str] = []
            text_buffer.append(f"All `{component}` cancelled.")
            for task_id in cancelled:
                text_buffer.append(f"- [{task_id}]")
            await send_msg.send_prompt(
                "\n".join(text_buffer),
            )
        else:
            await send_msg.send_error("Task not found.")