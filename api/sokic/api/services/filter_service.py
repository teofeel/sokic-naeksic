from abc import ABC, abstractmethod
from typing import List
from ..models import Graph, Node

class FilterService(ABC):

    @abstractmethod
    def filter_nodes(self, graph: Graph, filter_query: str) -> List[Node]:
        """
        Structured filter: <attribute> <comparator> <value>
        Raises FilterParseError for bad syntax, FilterTypeError for type mismatch.
        """
        pass

    @abstractmethod
    def filter_subgraph(self, graph: Graph, filter_query: str) -> Graph:
        """Return subgraph of matching nodes + edges between them."""
        pass