from sokic.api.models.graph import Graph
from sokic.api.services.Plugin import Plugin
import abc


class DataSourcePlugin(Plugin):

    @abc.abstractmethod
    def convert_to_graph(self, stream: str) -> Graph:
        """
        Convert from data source (JSON, YAML, ...) to graph model
        :param stream:
        :return: Graph model
        """
        pass
