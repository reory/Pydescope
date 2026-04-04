# PyVis interactive graph

from pyvis.network import Network 

MAX_NODES_DEFAULT = 200

class PyVisRenderer:
    def __init__(self, graph, max_nodes: int = MAX_NODES_DEFAULT):
        self.graph = graph
        self.max_nodes = max_nodes

    def render(self, output_path="pydescope.html"):
      node_count = self.graph.number_of_nodes()
      edge_count = self.graph.number_of_edges()

      # Guard clause important - bail early if graph is too large
      if node_count > self.max_nodes:
        raise ValueError(
          f"\n 🔴Graph to large to render safely!\n"
          f"    Nodes found: {node_count}\n"
          f"    Edges found: {edge_count}\n"
          f"    Limit      : {self.max_nodes}\n\n"
          f"    Tip: Run with --max-nodes {node_count} to force render,\n"
          f"    or point pydescope at a subdirectory instead."
        )


      net = Network(height="1200px", width="100%", directed=True)
        
      # Enable hierarchical layout
      net.set_options("""
      {
        "layout": {
          "hierarchical": {
            "enabled": true,
            "levelSeparation": 200,
            "nodeSpacing": 200,
            "treeSpacing": 250,
            "direction": "UD",
            "sortMethod": "hubsize"
          }
        },
        "physics": {
          "enabled": false,
          "hierarchicalRepulsion": {
            "centralGravity": 0.0
          }
        }
      }
      """)
        
      net.from_nx(self.graph)
      net.write_html(output_path)

      print(f"  Nodes: {node_count}")
      print(f"  Edge:  {edge_count}")
        
      return output_path