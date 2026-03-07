from typing import Optional

from sokic.api.services.WorkspaceRepository import WorkspaceRepository
from core.sokic.core.use_cases.Workspace import Workspace

class InMemoryWorkspaceRepository(WorkspaceRepository):
    """
    Implements Repository pattern for Workspace using InMemory
    """
    def __init__(self):
        self.workspaces: dict[str, Workspace] = {}


    def save(self, workspace: Workspace) -> bool:
        """
        Saves workspace to InMemory
        :param workspace:
        :return: True if saved else False
        """
        if workspace.id in self.workspaces:
            return False

        self.workspaces[workspace.id] = workspace
        return True

    def update(self, workspace: Workspace) -> bool:
        """
        Updates workspace with new data
        :param workspace:
        :return: Returns True if updated else False
        """
        if workspace.id not in self.workspaces:
            return False

        self.workspaces[workspace.id] = workspace
        return True

    def load_all(self) -> dict[str, Workspace]:
        return self.workspaces


    def load_by_id(self, workspace_id: str) -> Optional[Workspace]:
        if not workspace_id in self.workspaces:
            return None

        return self.workspaces[workspace_id]


    def load_by_name(self, workspace_name: str) -> Optional[Workspace]:
        for workspace in self.workspaces.values():
            if workspace_name == workspace.name:
                return workspace

        return None


    def remove(self, workspace_id: str) -> bool:
        """
        Removes workspace from InMemory
        :param workspace_id:
        :return: Returns True if removed else False
        """
        if not workspace_id in self.workspaces:
            return False

        self.workspaces.pop(workspace_id)
        return True
