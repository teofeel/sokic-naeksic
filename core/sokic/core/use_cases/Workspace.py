from sokic.api.services import DataSourcePlugin, VisualizerPlugin
from sokic.api.models import Graph
from core.sokic.core.use_cases.filter_service_impl import FilterServiceImpl
from core.sokic.core.use_cases.search_service_impl import SearchServiceImpl
from typing import Optional, List
import uuid

class Workspace:
    """
        Workspace is implemented as a Context class of Strategy Pattern
    """

    def __init__(self, name: str, graph: Graph):
        """
        :param name: Name of the workspace
        :param graph: Source Graph for this workspace
        """
        self.id = str(uuid.uuid4())
        self.name = name

        self.source_graph: Graph = graph
        self.active_graph: Graph = graph

        self.datasource: Optional[DataSourcePlugin] = None
        self.visualizer: Optional[VisualizerPlugin] = None

        self.filter_queries: List[str] = []
        self.search_query: Optional[str] = None

        self.filter_service = FilterServiceImpl()
        self.search_service = SearchServiceImpl()


    def set_datasource(self, datasource: DataSourcePlugin):
        """
        Sets the data source strategy used to fetch or refresh graph data
        :param datasource: Implementation of Datasource plugin
        :return:
        """
        self.datasource = datasource


    def set_visualizer(self, visualizer: VisualizerPlugin):
        """
        Sets the visualization strategy used to render the active graph
        :param visualizer: Implementation of Visualizer plugin
        :return:
        """
        self.visualizer = visualizer


    def add_filter(self, query: str) -> bool:
        """
        Add a filter query to this workspace
        :param query: Should be string expression representing the filter (e.g. 'age > 35')
        :return: True if the filter was added, False otherwise
        """
        if query in self.filter_queries:
            return False

        self.filter_queries.append(query)
        self.rebuild_graph()

        return True

    def set_filters(self, filters: List[str]) -> bool:
        """
        Sets filters for this workspace
        :param filters: List of filters
        :return: True if the filters were changed, False otherwise
        """
        if not filters:
            return False

        changed = False
        for query in filters:
            if query not in self.filter_queries:
                self.filter_queries.append(query)
                changed = True

        if changed:
            self.rebuild_graph()

        return changed


    def set_search(self, query: str):
        """
        Set search query to this workspace
        :param query: Search string used to filter nodes
        :return:
        """
        self.search_query = query
        self.rebuild_graph()


    def render(self) -> Optional[str]:
        """
        Creates html representation of active graph using assigned Visualizer
        :return:
        """
        if not self.visualizer:
            return None

        return self.visualizer.visualize(self.active_graph)


    def rebuild_graph(self):
        """
        Used to rebuild the graph, actually uses filter and search query to create new active graph
        :return:
        """
        temp_graph = self.source_graph

        for query in self.filter_queries:
            temp_graph = self.filter_service.filter_subgraph(temp_graph, query)

        if self.search_query:
            temp_graph = self.search_service.search_subgraph(temp_graph, self.search_query)

        self.active_graph = temp_graph


    def set_graph(self, graph: Graph):
        """
        Set new source graph
        :param graph: Generated graph
        :return:
        """
        self.source_graph = graph

    def get_filters(self) -> List[str]:
        """
        Get all active graph filters
        :return: List of all active graph filters
        """
        return self.filter_queries

    def get_search(self) -> str:
        """
        Get active graph search
        :return: Active search
        """
        return self.search_query
