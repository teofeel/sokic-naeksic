from graph_element import GraphElement
from edge import Edge
from node import Node

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_edge(self, edge: Edge):
        if edge.id in self.edges:
            return False
        
        if not (edge.source in self.nodes and edge.target in self.nodes):
            return False

        self.nodes[edge.source].out_edges.append(edge)
        self.nodes[edge.target].in_edges.append(edge)

        self.edges[edge.id] = edge
        return True
    
    def add_node(self, node: Node):
        if node.id in self.nodes:
            return False
        
        self.nodes[node.id] = node
        return True
    
    def remove_edge(self, key):
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
    
    def remove_node(self, key):
        if key not in self.nodes:
            return False
        
        for edge in self.edges.values():
            if edge.source == key or edge.target == key:
                return False

        del self.nodes[key]
        return True
    
    def update_edge(self, key, **data):
        if key not in self.edges:
            return False
        
        self.edges[key].update(**data)
        return True
    
    def update_node(self, key, **data):
        if key not in self.nodes:
            return False
        
        self.nodes[key].update(**data)
        return True
    
    def get_element(self, key):
        return self.nodes.get(key) or self.edges.get(key)
    
    def get_node(self, key):
        return self.nodes.get(key)

    def get_edge(self, key):
        return self.edges.get(key)

    def __getitem__(self, key):
        return self.nodes.get(key) or self.edges.get(key)
    

