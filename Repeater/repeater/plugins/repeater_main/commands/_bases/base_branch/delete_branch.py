from abc import abstractmethod

from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from .base_branch import BaseBranch
from ....clients import UserDataClient

class DeleteBranch(BaseBranch):
    @classmethod
    def documents(cls):
        docs = [
            "Delete the active branch file.",
            "",
            "Usage:",
            "```",
            f"/{cls.cmd}",
            "```"
        ]
        cls.description = "\n".join(docs)
        return cls.description
    
    async def parser(self, branch_id: str, client: UserDataClient, send_msg: SendMsg):
        response = await client.delete()
        await send_msg.send_response_check_code(response, f"Deleted active branch")