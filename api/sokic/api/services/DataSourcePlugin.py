from sokic.api.models.graph import Graph
from sokic.api.services.Plugin import Plugin
import abc


class DataSourcePlugin(Plugin):

    @abc.abstractmethod
    def convert_to_graph(self, filepath: str) -> Graph:
        """
        Convert from data source (JSON, YAML, ...) to graph model
        :param filepath:
        :return: Graph model
        """
        pass
