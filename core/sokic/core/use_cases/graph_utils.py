from typing import List
from sokic.api.models import Graph, Node

def build_subgraph(graph: Graph, nodes: List[Node]) -> Graph:
    node_ids = {n.id for n in nodes}
    sub = Graph(direction=graph.direction, cycle_policy=graph.cycle_policy)
    for node in nodes:
        sub.nodes[node.id] = node
    for edge in graph.edges.values():
        if edge.source in node_ids and edge.target in node_ids:
            sub.edges[edge.id] = edge
    return sub