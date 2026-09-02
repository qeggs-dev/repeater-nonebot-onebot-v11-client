from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from .base_branch import BaseBranch
from ....clients import UserDataClient

class BindBranchFrom(BaseBranch):
    @classmethod
    def documents(cls):
        docs = [
            "Hardlinks the specified branch and the active branch and uses the specified branch as the data source.",
            "If there is data in the active branch, the data will be overwritten.",
            "",
            "Usage:",
            "```",
            f"/{cls.cmd} branch_id",
            "```"
        ]
        cls.description = "\n".join(docs)
        return cls.description
    
    async def parser(self, branch_id: str, client: UserDataClient, send_msg: SendMsg):
        response = await client.bind_from(src_branch_id=branch_id)
        await send_msg.send_response_check_code(response, f"Branch {branch_id} has been bound to the current branch.")