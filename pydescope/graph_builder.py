# Networkx Graph
import networkx as nx 

class GraphBuilder:
    def __init__(self, edges):
        self.edges = edges

    def build(self):
        g = nx.DiGraph()
        g.add_edges_from(self.edges)
        return g
