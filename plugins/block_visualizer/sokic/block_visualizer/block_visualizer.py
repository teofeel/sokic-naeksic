from typing import Dict, Any
from sokic.api.models.edge import Edge
from sokic.api.models.graph import Graph
from sokic.api.models.node import Node
from sokic.api.services.visualizer_plugin import VisualizerPlugin


class BlockVisualizer(VisualizerPlugin):
    """
    Visualizer that passes all GraphElement data to D3.js to be
    rendered as blocks with all the neccessary info
    """

    def name(self) -> str:
        return "block"

    def type(self) -> str:
        return "visualizer"

    def _get_node_data(self, node: Node) -> Dict[str, Any]:
        return {"id": node.id, **node.data}

    def _get_edge_data(self, edge: Edge) -> Dict[str, Any]:
        return {
            "id": edge.id,
            "source": edge.source,
            "target": edge.target,
            **edge.data
        }

    def visualize(self, graph: Graph) -> str:

        """
        Generates visual representation of Graph object as HTML string
        :param graph:
        :return:
        """

        graph_data = self._graph_to_json(graph)

        print("direktovan: " + str(graph.is_directed()))

        return f"""
        <div id="graph-viewport" style="width: 100%; height: 100%; position: absolute; inset: 0;"></div>
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <script>
            (function() {{
                const data = {graph_data};
                
                const container = document.getElementById("graph-viewport");
                const width = container.clientWidth || 800;
                const height = container.clientHeight || 600;

                const svg = d3.select("#graph-viewport")
                    .append("svg")
                    .attr("width", "100%")
                    .attr("height", "100%");
                    
                const defs = svg.append("defs");

                defs.append("marker")
                    .attr("id", "arrowhead")
                    .attr("viewBox", "-0 -5 10 10")
                    .attr("refX", 5)
                    .attr("refY", 0)
                    .attr("orient", "auto")
                    .attr("markerWidth", 6)
                    .attr("markerHeight", 6)
                    .attr("xalign", "center")
                    .append("path")
                    .attr("d", "M 0,-5 L 10 ,0 L 0,5")
                    .attr("fill", "#000")
                    .style("stroke", "none");

                const simulation = d3.forceSimulation(data.nodes)
                    .force("link", d3.forceLink(data.links).id(d => d.id).distance(150))
                    .force("charge", d3.forceManyBody().strength(-400))
                    .force("center", d3.forceCenter(width / 2, height / 2));

                const link = svg.append("g")
                            .selectAll("path")
                            .data(data.links)
                            .join("path")
                            .attr("stroke", "#000")
                            .attr("stroke-width", 2)
                            .attr("fill", "none")
                    
                if ({1 if graph.is_directed() else 0})
                    link.attr("marker-mid", "url(#arrowhead)");

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

                const textBlock = node.append("text")
                    .attr("text-anchor", "middle")
                    .attr("font-family", "sans-serif")
                    .attr("font-size", "10px");

                textBlock.append("tspan")
                    .attr("x", 0)
                    .attr("dy", "0")
                    .style("font-weight", "bold")
                    .text(d => `ID: ${{d.id}}`);

                textBlock.each(function(d) {{
                    const el = d3.select(this);
                    const keys = Object.keys(d).filter(k => 
                        !['id', 'x', 'y', 'vx', 'vy', 'index', 'fx', 'fy'].includes(k)
                    );

                    keys.forEach(key => {{
                        el.append("tspan")
                            .attr("x", 0)
                            .attr("dy", "1.2em")
                            .text(`${{key}}: ${{d[key]}}`);
                    }});
                }});

                node.insert("rect", "text")
                    .each(function(d) {{
                        const g = d3.select(this.parentNode);
                        const bbox = g.select("text").node().getBBox();
                        const padding = 10;
                        
                        

                        d3.select(this)
                            .attr("x", bbox.x - padding)
                            .attr("y", bbox.y - padding)
                            .attr("width", bbox.width + (padding * 2))
                            .attr("height", bbox.height + (padding * 2))
                            .attr("rx", 5)
                            .attr("fill", "#fff")
                            .attr("stroke", "#333");
                    }});

                simulation.on("tick", () => {{
                    link.attr("d", d => {{
                        const mx = (d.source.x + d.target.x) / 2;
                        const my = (d.source.y + d.target.y) / 2;
                        return `M ${{d.source.x}},${{d.source.y}} L ${{mx}},${{my}} L ${{d.target.x}},${{d.target.y}}`;
                    }});

                    node.attr("transform", d => `translate(${{d.x}}, ${{d.y}})`);
                }});
            }})();
        </script>
        """