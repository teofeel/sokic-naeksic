import json
from typing import Dict, Any

from sokic.api.models.graph import Graph
from sokic.api.models.node import Node
from sokic.api.models.edge import Edge
from sokic.api.services.Plugin import Plugin
import abc


class VisualizerPlugin(Plugin):

    @abc.abstractmethod
    def _get_node_data(self, node: Node) -> Dict[str, Any]:
        """Subclasses define what node data goes to D3"""
        pass

    @abc.abstractmethod
    def _get_edge_data(self, edge: Edge) -> Dict[str, Any]:
        """Subclases define what edge data goes to D3"""
        pass

    def _graph_to_json(self, graph: Graph) -> str:
        """Generic loop that dumps data into json based on get data implementations"""
        return json.dumps({
            "nodes": [self._get_node_data(node) for node in graph.nodes.values()],
            "links": [self._get_edge_data(edge) for edge in graph.edges.values()]
        })

    @abc.abstractmethod
    def visualize(self, graph: Graph) -> str:
        """
        Converts a Graph object into a HTML string

        The result should contain the necessary HTML/JavaScript
        with D3.js to be injected directly
        into a Flask template using the `| safe` filter.

        Args:
            graph (Graph): The graph model instance containing nodes and edges
                to be visualized

        Returns:
            str: A string of HTML with <script> tags representing the visual
                graph ready for browser rendering
        """
        pass
