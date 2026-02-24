from graph_element import GraphElement
from edge import Edge
from node import Node

class Graph():
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_edge(self, edge: Edge):
        if edge.id in self.edges:
            return False
        
        if not (edge.source.id in self.nodes and edge.target.id in self.nodes):
            return False
        
        self.edges[edge.id] = edge
        return True
    
    def add_node(self, node: Node):
        if node.id in self.nodes:
            return False
        
        self.nodes[node.id] = node
        return True
    
    def remove_edge(self, id):
        if id not in self.edges:
            return False
        
        edge: Edge = self.edges[id]

        if edge in edge.source.out_edges:
            edge.source.out_edges.remove(edge)
        if edge in edge.target.in_edges:
            edge.target.in_edges.remove(edge)

        del self.edges[id]
        return True
    
    def remove_node(self, id):
        if id not in self.nodes:
            return False
        
        for edge in self.edges.values():
            if edge.source.id == id or edge.target.id == id:
                return False

        del self.nodes[id]
        return True
    
    def update_edge(self, id, **data):
        if id not in self.edges:
            return False
        
        self.edges[id].update(**data)
        return True
    
    def update_node(self, id, **data):
        if id not in self.nodes:
            return False
        
        self.nodes[id].update(**data)
        return True
    
    def get_element(self, key):
        return self.nodes.get(key) or self.edges.get(key)
    

    def __getitem__(self, key):
        return self.nodes.get(key) or self.edges.get(key)
    


