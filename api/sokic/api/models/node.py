from .graph_element import GraphElement

class Node(GraphElement):
    def __init__(self, id, **kwargs):
        super().__init__(id, **kwargs)

        self.out_edges = []
        self.in_edges = []