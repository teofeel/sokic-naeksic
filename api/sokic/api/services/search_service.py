from typing import List
from sokic.api.models.graph import Graph
from sokic.api.models.node import Node
from sokic.api.models.edge import Edge

class SearchService:
    """
    Full-text search for Graph objects.
    """

    # ── SEARCH ────────────────────────────────────────────────────────── #

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
        """Return a subgraph of nodes matching `query` + edges between them."""
        return self._build_subgraph(graph, self.search_nodes(graph, query))

    def search_edges(self, graph: Graph, query: str) -> List[Edge]:
        """
        Edges whose id, source id, target id, or any data value
        contains `query` (case-insensitive).
        """
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

