from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from .base_branch import BaseBranch
from ....clients import UserDataClient

class ChangeBranch(BaseBranch):
    @classmethod
    def documents(cls):
        docs = [
            "Switch the active branch.",
            "",
            "Usage:",
            "```",
            f"/{cls.cmd} branch_id",
            "```"
        ]
        cls.description = "\n".join(docs)
        return cls.description
    
    async def parser(self, branch_id: str, client: UserDataClient, send_msg: SendMsg):
        response = await client.change_branch(branch_id)
        await send_msg.send_response_check_code(response, f"The branch has been switched to {branch_id}")