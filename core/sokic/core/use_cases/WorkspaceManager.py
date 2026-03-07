from sokic.api.services.WorkspaceRepository import WorkspaceRepository
from sokic.api.models import Graph
from core.sokic.core.use_cases.plugin_loader import PluginLoader
from core.sokic.core.use_cases.Workspace import Workspace
from typing import List, Optional

class WorkspaceManager:
    """
    Implements Facade pattern
    """

    def __init__(self, plugin_loader: PluginLoader, repository: WorkspaceRepository):
        """
        :param plugin_loader: PluginLoader object used to load plugins
        """
        self.plugin_loader = plugin_loader
        self.repository: WorkspaceRepository = repository
        self.active_workspace_id: Optional[str] = None

    def create_workspace(self, name: str, graph: Graph, datasource_key: str, visualizer_key: str) -> str:
        """
        Used to create a new workspace
        :param name: Name of the workspace
        :param graph: Graph object
        :param datasource_key: String name of the datasource plugin
        :param visualizer_key: String name of the visualizer plugin
        :return: ID of the new workspace
        """

        datasource_plugin = self.plugin_loader.plugins['datasource'][datasource_key]
        if datasource_plugin is None:
            raise ValueError(f'Datasource plugin {datasource_key} not found')

        visualizer_plugin = self.plugin_loader.plugins['visualizer'][visualizer_key]
        if visualizer_plugin is None:
            raise ValueError(f'Visualizer plugin {visualizer_key} not found')

        workspace = Workspace(name, graph)

        workspace.set_datasource(datasource_plugin)
        workspace.set_visualizer(visualizer_plugin)

        self.repository.save(workspace)
        self.active_workspace_id = workspace.id

        return workspace.id

    def switch_workspace_id(self, workspace_id: str) -> bool:
        """
        Used to switch workspace
        :param workspace_id: ID of the workspace
        :return: True if switched, otherwise False
        """
        workspace = self.repository.load_by_id(workspace_id)
        if workspace is None:
            return False

        self.active_workspace_id = workspace_id
        return True

    def switch_workspace_name(self, workspace_name: str) -> bool:
        """
        Used to switch workspace
        :param workspace_id: ID of the workspace
        :return: True if switched, otherwise False
        """
        workspace = self.repository.load_by_name(workspace_name)
        if workspace is None:
            return False

        self.active_workspace_id = workspace.id
        return True


    def get_active_render(self) -> Optional[str]:
        """
        Returns HTML view of the graph with all its nodes and edges
        :return:
        """
        workspace = self.repository.load_by_id(self.active_workspace_id)
        if workspace is None:
            return None

        return workspace.render()


    def set_active_search(self, query: str):
        """
        Sets search to active workspace
        :return:
        """
        active_workspace = self.repository.load_by_id(self.active_workspace_id)
        if active_workspace:
            active_workspace.set_search(query)
            self.repository.update(active_workspace)


    def add_active_filter(self, query: str):
        """
        Adds filter query to active workspace
        :param query: Should be string expression representing the filter (e.g. 'age > 35')
        :return:
        """
        active_workspace = self.repository.load_by_id(self.active_workspace_id)
        if active_workspace:
            active_workspace.add_filter(query)
            self.repository.update(active_workspace)


    def set_active_visualizer(self, visualizer_key: str) -> bool:
        """
        Sets visualizer to active workspace
        :param visualizer_key: String name of the visualizer plugin
        :return: True if set, otherwise False
        """
        plugin = self.plugin_loader.plugins['visualizer'][visualizer_key]
        if plugin is None:
            return False

        active_workspace = self.repository.load_by_id(self.active_workspace_id)
        if active_workspace is None:
            return False

        active_workspace.set_visualizer(plugin)
        self.repository.update(active_workspace)
        return True


    def get_active_workspace(self) -> Optional[Workspace]:
        """
        Returns active workspace
        :return:
        """
        if self.active_workspace_id is None:
            return None

        return self.repository.load_by_id(self.active_workspace_id)

    def get_all_workspaces_metadata(self) -> List[dict]:
        """
        Returns a list of all loaded workspaces metadata
        :return: A list of dictionaries, each containing id, name, and is_active
        """
        metadata = []

        for id, workspace in self.repository.load_all().items():
            metadata.append({'id': id, 'name': workspace.name, "is_active": id == self.active_workspace_id})

        return metadata