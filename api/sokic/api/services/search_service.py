from abc import ABC, abstractmethod
from typing import List
from ..models import Graph, Node, Edge

class SearchService(ABC):

    @abstractmethod
    def search_nodes(self, graph: Graph, query: str) -> List[Node]:
        """Return nodes whose attribute names or values contain `query`."""
        pass

    @abstractmethod
    def search_subgraph(self, graph: Graph, query: str) -> Graph:
        """Return subgraph of matching nodes + edges between them."""
        pass

    @abstractmethod
    def search_edges(self, graph: Graph, query: str) -> List[Edge]:
        """Return edges whose id/source/target/data contains `query`."""
        pass