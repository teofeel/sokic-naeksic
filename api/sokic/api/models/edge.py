from .graph_element import GraphElement

class Edge(GraphElement):
    def __init__(self, id, source, target, **kwargs):
        super().__init__(id, **kwargs)

        self.source = source
        self.target = target