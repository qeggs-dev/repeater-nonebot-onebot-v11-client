from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from .base_branch import BaseBranch
from ....clients import UserDataClient

class CloneBranch(BaseBranch):
    @classmethod
    def documents(cls):
        docs = [
            "Clone the specified branch and the active branch and uses the active branch as the data source.",
            "If there is data in the specified branch, the data will be overwritten.",
            "",
            "Usage:",
            "```",
            f"/{cls.cmd} branch_id",
            "```"
        ]
        cls.description = "\n".join(docs)
        return cls.description
    
    async def parser(self, branch_id: str, client: UserDataClient, send_msg: SendMsg):
        response = await client.clone(branch_id)
        await send_msg.send_response_check_code(response, f"The current branch has been cloned into Branch {branch_id}.")