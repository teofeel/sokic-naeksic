from typing import Any, List, Tuple
from sokic.api.services import SearchService
from sokic.api.models import Graph, Node, Edge
from core.sokic.core.use_cases.graph_utils import build_subgraph


class SearchServiceImpl(SearchService):

    def search_nodes(self, graph: Graph, query: str) -> List[Node]:
        q = query.lower()
        result: List[Node] = []
        for node in graph.nodes.values():
            for attr_name, attr_value in node.data.items():
                if q in attr_name.lower() or q in str(attr_value).lower():
                    result.append(node)
                    break
        return result

    def search_subgraph(self, graph: Graph, query: str) -> Graph:
        return build_subgraph(graph, self.search_nodes(graph, query))

    def search_edges(self, graph: Graph, query: str) -> List[Edge]:
        q = query.lower()
        result: List[Edge] = []
        for edge in graph.edges.values():
            if q in edge.source.lower() or q in edge.target.lower() or q in edge.id.lower():
                result.append(edge)
                continue
            if hasattr(edge, "data") and edge.data:
                if any(q in str(v).lower() for v in edge.data.values()):
                    result.append(edge)
        return result

