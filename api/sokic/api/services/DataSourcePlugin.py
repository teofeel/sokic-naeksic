from sokic.api.models import Graph
from sokic.api.services import Plugin
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

    @abc.abstractmethod
    def _is_cyclic(self, data: dict) -> bool:
        """
        Checks if graph is cyclic
        :param data:
        :return:
        """
        pass

    @abc.abstractmethod
    def _is_directed(self, data: dict) -> bool:
        """
        Checks if graph is directed
        :param data:
        :return:
        """
        pass
