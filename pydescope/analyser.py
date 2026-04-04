# Build dependency edges

class DependencyAnalyser:
    def __init__(self, imports_map):
        self.imports_map = imports_map

    def build_edges(self):

        edges = []
        for module, imports in self.imports_map.items():
            for imp in imports:
                edges.append((module, imp))
        return edges