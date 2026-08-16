import uuid
from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)

@CommandCaller.register
class Cancel(CommandPackage):
    cmd = "cancel"
    aliases = {
        "cl",
        "CL",
        "Cancel",
        "CANCEL",
    }
    cmd_type = CmdTypes.CONTROL
    documents = f"""
    Cancel a task.

    Usage: 
        /{cmd} task_id
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        try:
            task_id = uuid.UUID(persona_info.message_striped_str)
        except ValueError:
            await send_msg("Invalid task id.")
        
        if task_id in CommandCaller.running_map.get(persona_info.namespace, set()):
            task = CommandCaller.runnings[task_id]
            component = task.package.component
            task.cancel()
            await send_msg.send_prompt(f"Task `{component}`({task_id}) cancelled.")
        else:
            await send_msg.send_error("Task not found.")