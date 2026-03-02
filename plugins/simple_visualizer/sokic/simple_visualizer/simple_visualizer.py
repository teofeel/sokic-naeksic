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
        """
        Generates visual representation of Graph object as HTML string
        :param graph:
        :return:
        """

        graph_data = self._graph_to_json(graph)

        return f"""
        <div id="graph-viewport" style="border: 1px solid #ccc;"></div>
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <script>
            (function() {{
                const data = {graph_data};
                const width = 800;
                const height = 600;
                const nodeRadius = 40;

                const svg = d3.select("#graph-viewport")
                    .append("svg")
                    .attr("viewBox", [0, 0, width, height]);

                // Arrow marker for directed edges
                svg.append("defs").append("marker")
                    .attr("id", "arrow")
                    .attr("viewBox", "0 -5 10 10")
                    .attr("refX", nodeRadius + 10)
                    .attr("refY", 0)
                    .attr("markerWidth", 6)
                    .attr("markerHeight", 6)
                    .attr("orient", "auto")
                    .append("path")
                    .attr("d", "M0,-5L10,0L0,5")
                    .attr("fill", "#999");

                const simulation = d3.forceSimulation(data.nodes)
                    .force("link", d3.forceLink(data.links).id(d => d.id).distance(150))
                    .force("charge", d3.forceManyBody().strength(-400))
                    .force("center", d3.forceCenter(width / 2, height / 2));

                const link = svg.append("g")
                    .selectAll("line")
                    .data(data.links)
                    .join("line")
                    .attr("stroke", "#999")
                    .attr("stroke-width", 2)
                    .attr("marker-end", "url(#arrow)");

                const node = svg.append("g")
                    .selectAll("g")
                    .data(data.nodes)
                    .join("g")
                    .call(d3.drag()
                        .on("start", (e, d) => {{
                            if (!e.active) simulation.alphaTarget(0.3).restart();
                            d.fx = d.x; d.fy = d.y;
                        }})
                        .on("drag", (e, d) => {{ d.fx = e.x; d.fy = e.y; }})
                        .on("end", (e, d) => {{
                            if (!e.active) simulation.alphaTarget(0);
                            d.fx = null; d.fy = null;
                        }}));

                // Circle background
                node.append("circle")
                    .attr("r", nodeRadius)
                    .attr("fill", "#fff")
                    .attr("stroke", "#333")
                    .attr("stroke-width", 2);

                // ID label centered in circle
                node.append("text")
                    .attr("text-anchor", "middle")
                    .attr("dominant-baseline", "middle")
                    .attr("font-family", "sans-serif")
                    .attr("font-size", "11px")
                    .attr("font-weight", "bold")
                    .text(d => d.id);

                simulation.on("tick", () => {{
                    link.attr("x1", d => d.source.x)
                        .attr("y1", d => d.source.y)
                        .attr("x2", d => d.target.x)
                        .attr("y2", d => d.target.y);

                    node.attr("transform", d => `translate(${{d.x}}, ${{d.y}})`);
                }});
            }})();
        </script>
        """