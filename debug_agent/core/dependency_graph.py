import networkx as nx
from typing import Dict


class DependencyGraph:
    """
    Directed graph representing file-level dependencies.
    Nodes: files
    Edges: file -> imported module
    """

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_file(self, file_path: str, metadata: Dict):
        """
        Add a file and its dependency to graph.
        """
        self.graph.add_node(file_path)

        for imp in metadata.get("imports", []):
            self.graph.add_edge(file_path, imp)
        
    def build(self, analyzer):
        """
        Build dependency graph from project analyzer.
        """

        files = analyzer.build_file_index()

        for file in files:
            metadata = analyzer.extract_metadata(file)
            self.add_file(file, metadata)

        return self.graph
    
    def save(self, path: str = "graph_adj.txt"):
        """
        Save graph adjacency list (for debugging).
        """
        nx.write_adjlist(self.graph, path)