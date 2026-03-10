from sokic.api.services.WorkspaceRepository import WorkspaceRepository
from sokic.api.models import Graph

from api.services import DataSourcePlugin
from core.sokic.core.use_cases.plugin_loader import PluginLoader
from core.sokic.core.use_cases.Workspace import Workspace
from typing import List, Optional

class WorkspaceManager:
    def __init__(self, plugin_loader: PluginLoader, repository: WorkspaceRepository):
        """
        :param plugin_loader: PluginLoader object used to load plugins
        """
        self.plugin_loader = plugin_loader
        self.repository: WorkspaceRepository = repository

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

        return workspace.id


    def get_render(self, workspace_id: str) -> Optional[str]:
        """
        Returns HTML view of the graph with all its nodes and edges
        :param workspace_id: ID of the Workspace
        :return:
        """
        workspace = self.repository.load_by_id(workspace_id)
        if workspace is None:
            return None

        return workspace.render()


    def set_search(self, query: str, workspace_id: str):
        """
        Sets search to active workspace
        :param query: Query for the search
        :param workspace_id: ID of the Workspace
        :return:
        """
        workspace = self.repository.load_by_id(workspace_id)
        if workspace:
            workspace.set_search(query)
            self.repository.update(workspace)


    def add_filter(self, query: str, workspace_id: str):
        """
        Adds filter query to active workspace
        :param query: Should be string expression representing the filter (e.g. 'age > 35')
        :param workspace_id: ID of the Workspace
        :return:
        """
        workspace = self.repository.load_by_id(workspace_id)
        if workspace:
            workspace.add_filter(query)
            self.repository.update(workspace)


    def set_visualizer(self, workspace_id: str, visualizer_key: str) -> bool:
        """
        Sets visualizer to active workspace
        :param visualizer_key: String name of the visualizer plugin
        :param workspace_id: ID of the Workspace
        :return: True if set, otherwise False
        """
        return self._set_workspace_plugin(workspace_id, 'visualizer', visualizer_key)

    def set_datasource(self, workspace_id: str, datasource_key: str):
        """
        Sets datasource to active workspace
        :param workspace_id: ID of the Workspace
        :param datasource_key: String name of the datasource plugin
        :return: True if set, otherwise False
        """
        return self._set_workspace_plugin(workspace_id, 'datasource', datasource_key)

    def _set_workspace_plugin(self, workspace_id: str, plugin_type: str, plugin_key: str) -> bool:
        plugin_category = self.plugin_loader.plugins.get(plugin_type, {})
        plugin = plugin_category.get(plugin_key)

        if plugin is None:
            return False

        workspace = self.repository.load_by_id(workspace_id)
        if workspace is None:
            return False

        if plugin_type == 'visualizer':
            workspace.set_visualizer(plugin)
        elif plugin_type == 'datasource':
            workspace.set_datasource(plugin)

        self.repository.update(workspace)
        return True

    def get_workspace(self, workspace_id: str) -> Optional[Workspace]:
        """
        Returns active workspace
        :param workspace_id: ID of the Workspace
        :return:
        """
        return self.repository.load_by_id(workspace_id)

    def get_all_workspaces_metadata(self) -> List[dict]:
        """
        Returns a list of all loaded workspaces metadata
        :return: A list of dictionaries, each containing id, name, and is_active
        """
        metadata = []

        for id, workspace in self.repository.load_all().items():
            metadata.append({'id': id, 'name': workspace.name})

        return metadata


    def set_new_graph(self, workspace_id: str, graph: Graph) -> bool:
        """
        Set new source graph for workspace
        :param workspace_id: ID of the Workspace
        :param graph: Generated graph
        :return:
        """
        workspace = self.repository.load_by_id(workspace_id)
        if not workspace:
            return False

        workspace.set_graph(graph)
        self.repository.update(workspace)
        return True

    def delete_workspace(self, workspace_id: str) -> bool:
        """
        Delete workspace
        :param workspace_id: ID of the Workspace
        :return: True if deleted, otherwise False
        """
        return self.repository.remove(workspace_id)

    def set_filters(self, workspace_id: str, filters: List[str]) -> bool:
        """
        Sets filters to active workspace
        :param workspace_id: ID of the Workspace
        :param filters: List of filters
        :return:
        """
        workspace = self.repository.load_by_id(workspace_id)
        if not workspace:
            return False

        success = workspace.set_filters(filters)
        if success:
            self.repository.update(workspace)

        return success

    def get_workspace_filters(self, workspace_id: str) -> List[str]:
        """
        Get active workspace filters
        :param workspace_id: ID of the Workspace
        :return: List of active filters
        """
        workspace = self.repository.load_by_id(workspace_id)
        if not workspace:
            return []

        return workspace.get_filters()

    def get_workspace_search(self, workspace_id: str) -> str:
        """
        Get active workspace search
        :param workspace_id: ID of the Workspace
        :return: Active search string
        """
        workspace = self.repository.load_by_id(workspace_id)
        if not workspace:
            return ""

        return workspace.get_search()
