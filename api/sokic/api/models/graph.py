from .edge import Edge
from .node import Node

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    # Add Edge function
    # Params: edge: Edge
    # Returns: bool
    def add_edge(self, edge: Edge)-> bool:
        if edge.id in self.edges:
            return False
        
        if not (edge.source in self.nodes
                and edge.target in self.nodes):
            return False

        self.nodes[edge.source].out_edges.append(edge)
        self.nodes[edge.target].in_edges.append(edge)

        self.edges[edge.id] = edge
        return True

    # Add Node function
    # Params: node: Node
    # Returns: bool
    def add_node(self, node: Node)-> bool:
        if node.id in self.nodes:
            return False
        
        self.nodes[node.id] = node
        return True

    # Removes Edge
    # Params: key: int | str
    # Returns: bool
    def remove_edge(self, key) -> bool:
        if key not in self.edges:
            return False
        
        edge: Edge = self.edges[key]

        node_source: Node = self.nodes[edge.source]
        node_target: Node = self.nodes[edge.target]

        if edge in node_source.out_edges:
            node_source.out_edges.remove(edge)
        if edge in node_target.in_edges:
            node_target.in_edges.remove(edge)

        del self.edges[key]
        return True

    # Removes Node
    # Params: key: int | str
    # Returns: bool
    def remove_node(self, key) -> bool:
        if key not in self.nodes:
            return False
        
        for edge in self.edges.values():
            if edge.source == key or edge.target == key:
                return False

        del self.nodes[key]
        return True

    # Updates Edge
    # Params: key: int | str, **data
    # Returns: bool
    def update_edge(self, key, **data) -> bool:
        if key not in self.edges:
            return False
        
        self.edges[key].update(**data)
        return True

    # Updates Node
    # Params: key: int | str, **data
    # Returns: bool
    def update_node(self, key, **data) -> bool:
        if key not in self.nodes:
            return False
        
        self.nodes[key].update(**data)
        return True

    # Get element of graph
    # Params: key: int | str
    # Returns: Edge | Node
    def get_element(self, key) -> Edge | Node | None:
        return self.nodes.get(key) or self.edges.get(key)

    # Get Node
    # Params: key: int | str
    # Returns: Node
    def get_node(self, key) -> Node:
        return self.nodes.get(key)

    # Get Edge
    # Params: key: int | str
    # Returns: Edge
    def get_edge(self, key) -> Edge:
        return self.edges.get(key)

    def __getitem__(self, key) -> Edge | Node | None:
        return self.nodes.get(key) or self.edges.get(key)

    def is_directed(self) -> bool:
        """
        Checks if the graph is directed or not
        True if it is directed
        False if it is undirected
        """
        for edge in self.edges.values():
            reverse_exists = any(
                e.source == edge.target and e.target == edge.source
                for e in self.nodes[edge.target].out_edges
            )
            if not reverse_exists:
                return True
        return False