from abc import ABC, abstractmethod

class WorkspaceRepository(ABC):
    @abstractmethod
    def save(self, workspace):
        """
        Implements save method
        :param workspace: Workspace object
        :return:
        """
        pass

    @abstractmethod
    def update(self, workspace):
        """
        Implements update method
        :param workspace: Workspace object
        :return:
        """
        pass

    @abstractmethod
    def load_by_id(self, workspace_id: str):
        """
        Loads Workspace object by workspace_id
        :param workspace_id: ID of the Workspace
        :return:
        """
        pass

    @abstractmethod
    def load_by_name(self, workspace_name: str):
        """
        Loads Workspace object by workspace_name
        :param workspace_name: Name of the Workspace
        :return:
        """
        pass

    @abstractmethod
    def load_all(self):
        """
        Loads all Workspace objects
        :return:
        """
        pass

    @abstractmethod
    def remove(self, workspace_id: str):
        """
        Removes Workspace object by workspace_id
        :param workspace_id: ID of the Workspace
        :return:
        """
        pass
