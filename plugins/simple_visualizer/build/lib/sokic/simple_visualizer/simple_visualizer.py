from typing import Dict, Any
import json

from sokic.api.models.graph import Graph
from sokic.api.models.node import Node
from sokic.api.models.edge import Edge
from sokic.api.services.VisualizerPlugin import VisualizerPlugin


class SimpleVisualizer(VisualizerPlugin):

    def name(self) -> str:
        return "simple"

    def type(self) -> str:
        return "visualizer"

    def _get_node_data(self, node: Node) -> Dict[str, Any]:
        return {
            "id": node.id
        }

    def _get_edge_data(self, edge: Edge) -> Dict[str, Any]:
        return {
            "source": edge.source,
            "target": edge.target
        }

    def visualize(self, graph: Graph) -> str:
        data = json.loads(self._graph_to_json(graph))

        nodes = "".join(
            f"<li>{n['id']}</li>"
            for n in data["nodes"]
        )

        edges = "".join(
            f"<li>{e['source']} → {e['target']}</li>"
            for e in data["links"]
        )

        return f"""
        <h3>Simple Visualizer</h3>

        <h4>Nodes</h4>
        <ul>{nodes}</ul>

        <h4>Edges</h4>
        <ul>{edges}</ul>
        """