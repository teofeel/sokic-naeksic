from api.sokic.models.graph_cycle import GraphCycle
from api.sokic.models.graph_direction import GraphDirection
from graph_element import GraphElement
from edge import Edge
from node import Node
from graph_direction import GraphDirection
from graph_cycle import GraphCycle

class Graph:
    def __init__(self, direction: GraphDirection, cycle_policy: GraphCycle):
        self.nodes = {}
        self.edges = {}
        self.direction = direction
        self.cycle_policy = cycle_policy

    # Add Edge function
    # Params: edge: Edge
    # Returns: bool
    def add_edge(self, edge: Edge)-> bool:
        if edge.id in self.edges:
            return False
        
        if not (edge.source in self.nodes
                and edge.target in self.nodes):
            return False

        if (self.direction == GraphDirection.UNDIRECTED
                and self.__is_already_connected(edge.source, edge.target)):
            return False

        if (self.cycle_policy == GraphCycle.ACYCLIC
                and self.__would_create_cycle(edge.source, edge.target)):
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


    # checks if adding edge between start and end would create cycle
    # Params: start_node: Node, end_node: Node
    # Returns: bool
    def __would_create_cycle(self, start_node: Node, end_node: Node) -> bool:
        if self.direction == GraphDirection.UNDIRECTED:
            return self.__has_path(start_node, end_node, set())
        else:
            return self.__has_path(end_node, start_node, set())

    # checks if there is already connection between start and end node
    # Params: start_node: Node, end_node: Node
    # Returns: bool
    def __is_already_connected(self, start_node: Node, end_node: Node) -> bool:
        source = self.nodes.get(start_node)
        if not source:
            return False

        for edge in source.out_edges:
            if edge.target == end_node or edge.source == end_node:
                return True

        for edge in source.in_edges:
            if edge.target == end_node or edge.source == end_node:
                return True

        return False

    # using dfs we traverse through graph
    # Params: start_node: Node, end_node: Node, visited: set, last_edge: id (Default None)
    # Returns: bool
    def __has_path(self, start_node: Node, end_node: Node, visited: set, last_edge=None) -> bool:
        if start_node == end_node:
            return True

        if start_node not in visited:
            visited.add(start_node)

        node = self.nodes[start_node]
        edges_to_check = list(node.out_edges)

        if self.direction == GraphDirection.UNDIRECTED:
            edges_to_check.extend(node.in_edges)

        for edge in edges_to_check:
            if edge.id == last_edge:
                continue

            neighbor_id = edge.target if edge.source == start_node else edge.source

            if neighbor_id not in visited:
                if self.__has_path(neighbor_id, end_node, visited, edge.id):
                    return True
        return False

